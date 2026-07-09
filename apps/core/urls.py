from django.urls import path

from .views import (
    AiDisclaimerView,
    DashboardView,
    HealthcareDisclaimerView,
    HealthCheckView,
    HomeView,
    ImpactView,
    PrivacyView,
    RetentionPolicyView,
    SecurityView,
    TermsView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("impact/", ImpactView.as_view(), name="impact"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("security/", SecurityView.as_view(), name="security"),
    path("healthcare-disclaimer/", HealthcareDisclaimerView.as_view(), name="healthcare_disclaimer"),
    path("ai-disclaimer/", AiDisclaimerView.as_view(), name="ai_disclaimer"),
    path("retention/", RetentionPolicyView.as_view(), name="retention"),
    path("health/", HealthCheckView.as_view(), name="health"),
]
