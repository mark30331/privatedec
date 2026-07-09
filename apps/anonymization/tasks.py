import logging

from celery import shared_task

from .services import mark_processing_failure, process_upload_session

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(), retry_backoff=True, retry_jitter=True)
def anonymize_upload_session(self, session_id):
    logger.info("Anonymization task queued for session %s", session_id)
    try:
        session = process_upload_session(session_id, task_id=self.request.id or "")
    except Exception as exc:
        logger.exception("Anonymization failed for session %s", session_id)
        mark_processing_failure(session_id, exc)
        raise
    return {"session_id": str(session.pk), "status": session.status}
