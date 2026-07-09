from django.urls import path

from .views import (
    DeleteSessionView,
    ProcessingDetailView,
    ProcessingStatusView,
    RetryIncreaseTView,
    ResultDetailView,
    ResultDownloadView,
    ResultReportView,
    StartProcessingView,
)

app_name = "results"

urlpatterns = [
    path("sessions/<uuid:pk>/process/", StartProcessingView.as_view(), name="start"),
    path("sessions/<uuid:pk>/retry-t/", RetryIncreaseTView.as_view(), name="retry_t"),
    path("sessions/<uuid:pk>/processing/", ProcessingDetailView.as_view(), name="processing"),
    path("sessions/<uuid:pk>/status/", ProcessingStatusView.as_view(), name="status"),
    path("sessions/<uuid:pk>/delete/", DeleteSessionView.as_view(), name="delete"),
    path("results/<uuid:pk>/", ResultDetailView.as_view(), name="detail"),
    path("results/<uuid:pk>/report/", ResultReportView.as_view(), name="report"),
    path("results/<uuid:pk>/download/", ResultDownloadView.as_view(), name="download"),
]
