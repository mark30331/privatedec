import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView

from apps.anonymization.models import AnonymizationRun
from apps.evidence.models import UsageEvent

from .forms import ColumnSelectionForm, UploadCSVForm
from .models import SessionStatus, UploadSchema, UploadSession
from .services import analyze_csv_upload, build_original_storage_key, persist_original_upload

logger = logging.getLogger(__name__)


class UploadCreateView(LoginRequiredMixin, FormView):
    template_name = "uploads/upload.html"
    form_class = UploadCSVForm
    success_url = reverse_lazy("uploads:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_sessions"] = self.request.user.upload_sessions.select_related("schema")[:5]
        return context

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["csv_file"]

        try:
            analysis = analyze_csv_upload(uploaded_file)
        except ValidationError as exc:
            form.add_error("csv_file", exc.message)
            return self.form_invalid(form)

        if form.cleaned_data["k_value"] > analysis["row_count"]:
            form.add_error("k_value", "k-anonymity cannot exceed the number of CSV rows.")
            return self.form_invalid(form)

        session = UploadSession(
            user=self.request.user,
            original_filename=uploaded_file.name,
            content_type=uploaded_file.content_type or "text/csv",
            file_size_bytes=uploaded_file.size,
            encoding=analysis["encoding"],
            delimiter=analysis["delimiter"],
            row_count=analysis["row_count"],
            column_count=analysis["column_count"],
            status=SessionStatus.READY,
            progress_percent=10,
        )
        storage_key = build_original_storage_key(
            self.request.user.pk,
            session.id,
            uploaded_file.name,
        )
        try:
            saved_key = persist_original_upload(storage_key, analysis["raw_bytes"])
            session.stored_original_key = saved_key
            with transaction.atomic():
                session.save()
                UploadSchema.objects.create(
                    session=session,
                    detected_columns_json=analysis["columns"],
                    detected_types_json=analysis["types"],
                    preview_rows_json=analysis["preview_rows"],
                    column_stats_json=analysis["column_stats"],
                )
                AnonymizationRun.objects.create(
                    session=session,
                    k_value=form.cleaned_data["k_value"],
                    l_value=form.cleaned_data["l_value"],
                    t_value=form.cleaned_data["t_value"],
                )
                UsageEvent.objects.create(
                    user=self.request.user,
                    session=session,
                    event_type="UPLOAD_CREATED",
                    metadata_json={"filename": uploaded_file.name, "row_count": analysis["row_count"]},
                )
        except Exception as exc:
            logger.exception("Failed to persist upload session for user %s", self.request.user.pk)
            form.add_error(
                "csv_file",
                "The file could not be stored. Check the configured object storage permissions and try again.",
            )
            messages.error(
                self.request,
                "Upload failed because the storage backend rejected the file.",
            )
            return self.form_invalid(form)

        messages.success(
            self.request,
            "CSV uploaded successfully. Review the detected columns and privacy settings.",
        )
        return redirect("uploads:detail", pk=session.pk)


class UploadSessionListView(LoginRequiredMixin, ListView):
    template_name = "uploads/session_list.html"
    context_object_name = "sessions"
    paginate_by = 10

    def get_queryset(self):
        return (
            UploadSession.objects.filter(user=self.request.user)
            .select_related("schema", "anonymization_run")
            .order_by("-created_at")
        )


class UploadSessionDetailView(LoginRequiredMixin, DetailView):
    template_name = "uploads/session_detail.html"
    model = UploadSession
    context_object_name = "session"

    def get_queryset(self):
        return (
            UploadSession.objects.filter(user=self.request.user)
            .select_related("schema", "anonymization_run")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schema = self.object.schema
        now = timezone.now()
        original_expires_at = self.object.created_at + timedelta(days=settings.ORIGINAL_RETENTION_DAYS)
        if self.object.processing_completed_at:
            result_base = self.object.processing_completed_at
        else:
            result_base = self.object.created_at
        result_expires_at = result_base + timedelta(days=settings.RESULT_RETENTION_DAYS)

        form = kwargs.get("selection_form")
        if form is None:
            form = ColumnSelectionForm(
                columns=schema.detected_columns_json,
                initial={
                    "quasi_identifier_columns": schema.quasi_identifier_columns_json,
                    "sensitive_columns": schema.sensitive_columns_json,
                },
            )
        context["column_summaries"] = self._build_column_summaries(schema)
        context["preview_table"] = self._build_preview_table(schema)
        context["selection_form"] = form
        context["status_badge_class"] = self._status_badge_class(self.object.status)
        context["original_expires_at"] = original_expires_at
        context["result_expires_at"] = result_expires_at
        context["original_expired"] = now >= original_expires_at
        context["result_expired"] = now >= result_expires_at
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ColumnSelectionForm(
            request.POST,
            columns=self.object.schema.detected_columns_json,
        )
        if form.is_valid():
            self.object.schema.quasi_identifier_columns_json = form.cleaned_data[
                "quasi_identifier_columns"
            ]
            self.object.schema.sensitive_columns_json = form.cleaned_data["sensitive_columns"]
            self.object.schema.save(
                update_fields=[
                    "quasi_identifier_columns_json",
                    "sensitive_columns_json",
                    "updated_at",
                ]
            )
            UsageEvent.objects.create(
                user=request.user,
                session=self.object,
                event_type="UPLOAD_VALIDATED",
                metadata_json={
                    "quasi_identifiers": self.object.schema.quasi_identifier_columns_json,
                    "sensitive_columns": self.object.schema.sensitive_columns_json,
                },
            )
            messages.success(request, "Column selections saved.")
            return redirect("uploads:detail", pk=self.object.pk)

        messages.error(request, "Please fix the column selection errors below.")
        context = self.get_context_data(selection_form=form)
        return self.render_to_response(context)

    def _build_column_summaries(self, schema):
        summaries = []
        for column in schema.detected_columns_json:
            stats = schema.column_stats_json.get(column, {})
            sample_values = stats.get("sample_values", [])
            summaries.append(
                {
                    "name": column,
                    "detected_type": schema.detected_types_json.get(column, "-"),
                    "unique_count": stats.get("unique_count", 0),
                    "min_display": stats.get("min") or (sample_values[0] if sample_values else "-"),
                    "max_display": stats.get("max")
                    or (sample_values[1] if len(sample_values) > 1 else "-"),
                }
            )
        return summaries

    def _build_preview_table(self, schema):
        preview_rows = []
        for row in schema.preview_rows_json:
            preview_rows.append([row.get(column, "") for column in schema.detected_columns_json])
        return preview_rows

    def _status_badge_class(self, status):
        return {
            SessionStatus.READY: "secondary",
            SessionStatus.PENDING: "warning",
            SessionStatus.PROCESSING: "info",
            SessionStatus.COMPLETED: "success",
            SessionStatus.FAILED: "danger",
        }.get(status, "secondary")
