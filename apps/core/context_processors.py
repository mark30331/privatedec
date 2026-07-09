from django.conf import settings


def policy(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Privatedec"),
        "SITE_CONTACT_EMAIL": getattr(settings, "SITE_CONTACT_EMAIL", "support@privatedec.local"),
        "LEGAL_LAST_UPDATED": getattr(settings, "LEGAL_LAST_UPDATED", ""),
        "ORIGINAL_RETENTION_DAYS": getattr(settings, "ORIGINAL_RETENTION_DAYS", 7),
        "RESULT_RETENTION_DAYS": getattr(settings, "RESULT_RETENTION_DAYS", 30),
        "SESSION_RETENTION_DAYS": getattr(settings, "SESSION_RETENTION_DAYS", 365),
    }

