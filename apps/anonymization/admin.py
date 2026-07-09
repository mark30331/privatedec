from django.contrib import admin

from .models import AnonymizationRun


@admin.register(AnonymizationRun)
class AnonymizationRunAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "engine_name",
        "k_value",
        "l_value",
        "t_value",
        "privacy_score",
        "processing_time_ms",
        "created_at",
    )
    list_filter = ("engine_name", "created_at")
    search_fields = ("session__original_filename", "session__user__email", "task_id")
