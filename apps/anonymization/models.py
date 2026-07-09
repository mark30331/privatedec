import uuid

from django.db import models


class AnonymizationRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(
        "uploads.UploadSession",
        on_delete=models.CASCADE,
        related_name="anonymization_run",
    )
    engine_name = models.CharField(max_length=100, default="planned")
    engine_version = models.CharField(max_length=50, blank=True)
    k_value = models.PositiveIntegerField(default=2)
    l_value = models.PositiveIntegerField(default=2)
    t_value = models.DecimalField(max_digits=4, decimal_places=3, default=0.200)
    suppression_placeholder = models.CharField(max_length=50, default="*")
    privacy_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    rows_processed = models.PositiveIntegerField(default=0)
    suppressed_rows = models.PositiveIntegerField(default=0)
    suppressed_cells = models.PositiveIntegerField(default=0)
    processing_time_ms = models.PositiveIntegerField(default=0)
    result_filename = models.CharField(max_length=255, blank=True)
    stored_result_key = models.CharField(max_length=500, blank=True)
    result_row_count = models.PositiveIntegerField(default=0)
    task_id = models.CharField(max_length=255, blank=True)
    failure_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Anonymization run for {self.session_id}"
