from django.contrib import admin

from .models import Testimonial, UsageEvent


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("title", "body", "user__email")


@admin.register(UsageEvent)
class UsageEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user", "session", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("user__email", "session__original_filename")
