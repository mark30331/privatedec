from datetime import timedelta

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.uploads.models import SessionStatus, UploadSession


class Command(BaseCommand):
    help = "Delete stored objects that exceed the configured retention windows."

    def handle(self, *args, **options):
        now = timezone.now()
        original_cutoff = now - timedelta(days=settings.ORIGINAL_RETENTION_DAYS)
        result_cutoff = now - timedelta(days=settings.RESULT_RETENTION_DAYS)
        session_cutoff = now - timedelta(days=settings.SESSION_RETENTION_DAYS)

        sessions = UploadSession.objects.select_related("anonymization_run").all()

        original_deleted = 0
        result_deleted = 0
        sessions_deleted = 0

        for session in sessions.iterator():
            changed_fields = set()
            original_key = session.stored_original_key
            try:
                run = session.anonymization_run
            except Exception:
                run = None
            result_key = getattr(run, "stored_result_key", "") if run else ""

            if original_key and session.created_at <= original_cutoff:
                try:
                    default_storage.delete(original_key)
                except Exception:
                    pass
                session.stored_original_key = ""
                changed_fields.add("stored_original_key")

                if session.status in {
                    SessionStatus.PENDING,
                    SessionStatus.VALIDATING,
                    SessionStatus.READY,
                    SessionStatus.PROCESSING,
                }:
                    session.status = SessionStatus.DELETED
                    session.error_code = "ORIGINAL_EXPIRED"
                    session.error_message = (
                        "The original uploaded file expired under the retention policy and can no longer be processed."
                    )
                    session.progress_percent = 100
                    changed_fields.update({"status", "error_code", "error_message", "progress_percent"})

                original_deleted += 1

            result_base = session.processing_completed_at or session.created_at
            if result_key and result_base and result_base <= result_cutoff:
                try:
                    default_storage.delete(result_key)
                except Exception:
                    pass
                if run:
                    run.stored_result_key = ""
                    run.save(update_fields=["stored_result_key", "updated_at"])
                if session.status == SessionStatus.COMPLETED:
                    session.error_code = "RESULT_EXPIRED"
                    changed_fields.add("error_code")
                result_deleted += 1

            if session.created_at <= session_cutoff:
                current_result_key = getattr(run, "stored_result_key", "") if run else ""
                if not session.stored_original_key and not current_result_key:
                    with transaction.atomic():
                        session.delete()
                    sessions_deleted += 1
                    continue

            if changed_fields:
                session.save(update_fields=list(changed_fields) + ["updated_at"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Retention cleanup finished. original_deleted={original_deleted} result_deleted={result_deleted} sessions_deleted={sessions_deleted}"
            )
        )

