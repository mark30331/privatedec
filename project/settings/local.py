from .base import *  # noqa: F403,F401

DEBUG = True

DATABASES = {
    "default": env.db(  # noqa: F405
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'local.sqlite3'}",  # noqa: F405
    )
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
