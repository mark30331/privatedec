from django.contrib import admin

from .models import UploadSchema, UploadSession


@admin.register(UploadSession)
class UploadSessionAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "user",
        "status",
        "row_count",
        "column_count",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("original_filename", "user__email", "stored_original_key")


@admin.register(UploadSchema)
class UploadSchemaAdmin(admin.ModelAdmin):
    list_display = ("session", "created_at", "updated_at")
    search_fields = ("session__original_filename", "session__user__email")
