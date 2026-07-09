from django.urls import path

from .views import UploadCreateView, UploadSessionDetailView, UploadSessionListView

app_name = "uploads"

urlpatterns = [
    path("upload/", UploadCreateView.as_view(), name="create"),
    path("sessions/", UploadSessionListView.as_view(), name="list"),
    path("sessions/<uuid:pk>/", UploadSessionDetailView.as_view(), name="detail"),
]
