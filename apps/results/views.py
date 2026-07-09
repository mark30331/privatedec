import os
import logging
from decimal import Decimal
from datetime import timedelta
from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, View

from apps.anonymization.services import build_result_preview
from apps.anonymization.tasks import anonymize_upload_session
from apps.evidence.models import UsageEvent
from apps.uploads.models import SessionStatus, UploadSession

logger = logging.getLogger(__name__)


def _user_session_queryset(user):
    return UploadSession.objects.filter(user=user).select_related("schema", "anonymization_run")


def _status_badge_class(status):
    return {
        SessionStatus.READY: "secondary",
        SessionStatus.PENDING: "warning",
        SessionStatus.PROCESSING: "info",
        SessionStatus.COMPLETED: "success",
        SessionStatus.FAILED: "danger",
    }.get(status, "secondary")


class StartProcessingView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(_user_session_queryset(request.user), pk=pk)
        if session.status == SessionStatus.PROCESSING:
            messages.info(request, "This session is already processing.")
            return redirect("results:processing", pk=session.pk)
        if session.status == SessionStatus.COMPLETED:
            messages.info(request, "This session has already been processed.")
            return redirect("results:detail", pk=session.pk)
        if not session.schema.quasi_identifier_columns_json:
            messages.error(request, "Select at least one quasi-identifier before processing.")
            return redirect("uploads:detail", pk=session.pk)
        if not session.schema.sensitive_columns_json:
            messages.error(request, "Select at least one sensitive attribute before processing.")
            return redirect("uploads:detail", pk=session.pk)

        session.status = SessionStatus.PENDING
        session.progress_percent = 0
        session.error_code = ""
        session.error_message = ""
        session.save(
            update_fields=[
                "status",
                "progress_percent",
                "error_code",
                "error_message",
                "updated_at",
            ]
        )

        task_result = anonymize_upload_session.delay(str(session.pk))
        session.anonymization_run.task_id = task_result.id or ""
        session.anonymization_run.save(update_fields=["task_id", "updated_at"])

        messages.success(request, "Processing started.")
        return redirect("results:processing", pk=session.pk)


class RetryIncreaseTView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(_user_session_queryset(request.user), pk=pk)
        if session.status == SessionStatus.PROCESSING:
            messages.info(request, "This session is already processing.")
            return redirect("results:processing", pk=session.pk)
        if session.status == SessionStatus.COMPLETED:
            messages.info(request, "This session has already been processed.")
            return redirect("results:detail", pk=session.pk)

        run = session.anonymization_run
        current_t = float(run.t_value or Decimal("0.200"))
        next_t = min(1.0, current_t + 0.2)
        run.t_value = Decimal(f"{next_t:.3f}")
        run.save(update_fields=["t_value", "updated_at"])

        session.status = SessionStatus.PENDING
        session.progress_percent = 0
        session.error_code = ""
        session.error_message = ""
        session.save(
            update_fields=[
                "status",
                "progress_percent",
                "error_code",
                "error_message",
                "updated_at",
            ]
        )

        task_result = anonymize_upload_session.delay(str(session.pk))
        session.anonymization_run.task_id = task_result.id or ""
        session.anonymization_run.save(update_fields=["task_id", "updated_at"])

        messages.success(request, f"Retrying with t-closeness = {run.t_value}.")
        return redirect("results:processing", pk=session.pk)


class ProcessingDetailView(LoginRequiredMixin, DetailView):
    template_name = "results/processing.html"
    context_object_name = "session"
    model = UploadSession

    def get_queryset(self):
        return _user_session_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_badge_class"] = _status_badge_class(self.object.status)
        return context


class ProcessingStatusView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        session = get_object_or_404(_user_session_queryset(request.user), pk=pk)
        return JsonResponse(
            {
                "status": session.status,
                "progress_percent": session.progress_percent,
                "error_message": session.error_message,
                "status_badge_class": _status_badge_class(session.status),
                "result_url": reverse("results:detail", kwargs={"pk": session.pk}),
            }
        )


class ResultDetailView(LoginRequiredMixin, DetailView):
    template_name = "results/detail.html"
    context_object_name = "session"
    model = UploadSession

    def get_queryset(self):
        return _user_session_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_badge_class"] = _status_badge_class(self.object.status)
        preview_rows = build_result_preview(self.object) if self.object.status == SessionStatus.COMPLETED else []
        context["result_preview"] = preview_rows
        context["result_columns"] = self.object.schema.detected_columns_json
        context["result_preview_table"] = [
            [row.get(column, "") for column in context["result_columns"]] for row in preview_rows
        ]
        now = timezone.now()
        if self.object.processing_completed_at:
            base = self.object.processing_completed_at
        else:
            base = self.object.created_at
        result_expires_at = base + timedelta(days=settings.RESULT_RETENTION_DAYS)
        context["result_expires_at"] = result_expires_at
        context["result_expired"] = now >= result_expires_at
        context["can_download"] = bool(self.object.anonymization_run.stored_result_key)
        return context


class ResultReportView(LoginRequiredMixin, DetailView):
    template_name = "results/report.html"
    context_object_name = "session"
    model = UploadSession

    def get_queryset(self):
        return _user_session_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        run = session.anonymization_run

        context["status_badge_class"] = _status_badge_class(session.status)
        context["generated_at"] = timezone.now()
        context["can_download"] = bool(run.stored_result_key)

        original_expires_at = session.created_at + timedelta(days=settings.ORIGINAL_RETENTION_DAYS)
        result_base = session.processing_completed_at or session.created_at
        result_expires_at = result_base + timedelta(days=settings.RESULT_RETENTION_DAYS)

        context["original_expires_at"] = original_expires_at
        context["result_expires_at"] = result_expires_at
        context["original_expired"] = timezone.now() >= original_expires_at
        context["result_expired"] = timezone.now() >= result_expires_at

        preview_rows = build_result_preview(session) if session.status == SessionStatus.COMPLETED else []
        context["result_preview"] = preview_rows
        context["result_columns"] = session.schema.detected_columns_json
        context["result_preview_table"] = [
            [row.get(column, "") for column in context["result_columns"]] for row in preview_rows
        ]
        return context


class ResultDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        session = get_object_or_404(_user_session_queryset(request.user), pk=pk)
        run = session.anonymization_run
        if session.status != SessionStatus.COMPLETED or not run.stored_result_key:
            messages.error(request, "The result file is not ready yet.")
            return redirect("results:detail", pk=session.pk)

        UsageEvent.objects.create(user=request.user, session=session, event_type="RESULT_DOWNLOADED")
        if settings.USE_R2:
            download_url = default_storage.url(
                run.stored_result_key,
                parameters={
                    "ResponseContentDisposition": (
                        f"attachment; filename*=UTF-8''{quote(run.result_filename or session.original_filename)}"
                    )
                },
                expire=settings.R2_SIGNED_URL_TTL,
            )
            return redirect(download_url)

        stored_file = default_storage.open(run.stored_result_key, "rb")
        return FileResponse(
            stored_file,
            as_attachment=True,
            filename=run.result_filename or os.path.basename(run.stored_result_key),
        )


class DeleteSessionView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(_user_session_queryset(request.user), pk=pk)
        original_key = session.stored_original_key
        result_key = session.anonymization_run.stored_result_key
        filename = session.original_filename

        for storage_key in (result_key, original_key):
            if not storage_key:
                continue
            try:
                default_storage.delete(storage_key)
            except Exception:
                logger.exception("Failed to delete storage object %s for session %s", storage_key, session.pk)

        with transaction.atomic():
            session.delete()

        messages.success(request, f'Deleted session "{filename}" and attempted file cleanup.')
        return redirect("uploads:list")
