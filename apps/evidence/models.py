import uuid

from django.conf import settings
from django.db import models


class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="testimonials",
    )
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.rating}/5)"


class UsageEvent(models.Model):
    EVENT_CHOICES = [
        ("USER_REGISTERED", "User Registered"),
        ("EMAIL_VERIFIED", "Email Verified"),
        ("UPLOAD_CREATED", "Upload Created"),
        ("UPLOAD_VALIDATED", "Upload Validated"),
        ("JOB_STARTED", "Job Started"),
        ("JOB_COMPLETED", "Job Completed"),
        ("JOB_FAILED", "Job Failed"),
        ("RESULT_DOWNLOADED", "Result Downloaded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usage_events",
    )
    session = models.ForeignKey(
        "uploads.UploadSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usage_events",
    )
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    metadata_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.event_type
