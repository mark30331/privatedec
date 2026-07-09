from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, View

from apps.anonymization.models import AnonymizationRun
from apps.uploads.models import SessionStatus, UploadSession


class HomeView(TemplateView):
    template_name = "core/home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"


class SecurityView(TemplateView):
    template_name = "core/security.html"


class HealthcareDisclaimerView(TemplateView):
    template_name = "core/healthcare_disclaimer.html"


class AiDisclaimerView(TemplateView):
    template_name = "core/ai_disclaimer.html"


class RetentionPolicyView(TemplateView):
    template_name = "core/retention.html"


class ImpactView(TemplateView):
    template_name = "core/impact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["as_of"] = timezone.now()
        context["total_sessions"] = UploadSession.objects.count()
        context["total_rows_uploaded"] = (
            UploadSession.objects.aggregate(total=models.Sum("row_count")).get("total") or 0
        )
        context["completed_runs"] = AnonymizationRun.objects.filter(
            session__status=SessionStatus.COMPLETED
        ).count()
        context["failed_runs"] = AnonymizationRun.objects.filter(
            session__status=SessionStatus.FAILED
        ).count()
        context["downloads"] = AnonymizationRun.objects.exclude(stored_result_key="").count()
        return context


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        try:
            connection.ensure_connection()
            database = "ok"
        except Exception:
            database = "error"

        status_code = 200 if database == "ok" else 503
        return JsonResponse(
            {"status": "ok" if status_code == 200 else "error", "database": database},
            status=status_code,
        )
