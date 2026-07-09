import uuid

from django.conf import settings
from django.db import models


class SessionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    VALIDATING = "VALIDATING", "Validating"
    READY = "READY", "Ready"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    DELETED = "DELETED", "Deleted"


class UploadSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="upload_sessions",
    )
    original_filename = models.CharField(max_length=255)
    stored_original_key = models.CharField(max_length=500, blank=True)
    content_type = models.CharField(max_length=255, blank=True)
    file_size_bytes = models.PositiveBigIntegerField(default=0)
    encoding = models.CharField(max_length=64, blank=True)
    delimiter = models.CharField(max_length=10, blank=True)
    row_count = models.PositiveIntegerField(default=0)
    column_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.PENDING,
    )
    progress_percent = models.PositiveSmallIntegerField(default=0)
    error_code = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.original_filename} ({self.status})"


class UploadSchema(models.Model):
    session = models.OneToOneField(
        UploadSession,
        on_delete=models.CASCADE,
        related_name="schema",
    )
    detected_columns_json = models.JSONField(default=list, blank=True)
    detected_types_json = models.JSONField(default=dict, blank=True)
    quasi_identifier_columns_json = models.JSONField(default=list, blank=True)
    sensitive_columns_json = models.JSONField(default=list, blank=True)
    preview_rows_json = models.JSONField(default=list, blank=True)
    column_stats_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "upload schemas"

    def __str__(self):
        return f"Schema for {self.session.original_filename}"
