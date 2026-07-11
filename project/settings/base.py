from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_VERIFICATION_REQUIRED=(bool, False),
    CELERY_TASK_ALWAYS_EAGER=(bool, False),
    CSV_MAX_UPLOAD_MB=(int, 50),
    SITE_NAME=(str, "Privatedec"),
    SITE_CONTACT_EMAIL=(str, "support@privatedec.local"),
    LEGAL_LAST_UPDATED=(str, ""),
    ORIGINAL_RETENTION_DAYS=(int, 7),
    RESULT_RETENTION_DAYS=(int, 30),
    SESSION_RETENTION_DAYS=(int, 365),
    USE_R2=(bool, False),
    R2_SIGNED_URL_TTL=(int, 3600),
)

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="django-insecure-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["storages"]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.uploads",
    "apps.anonymization",
    "apps.results",
    "apps.evidence",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.policy",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "project.asgi.application"

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"
LOGIN_URL = "accounts:login"

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@privatedec.local")
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_VERIFICATION_REQUIRED = env("EMAIL_VERIFICATION_REQUIRED")

CSV_MAX_UPLOAD_MB = env("CSV_MAX_UPLOAD_MB")
CSV_MAX_UPLOAD_BYTES = CSV_MAX_UPLOAD_MB * 1024 * 1024

SITE_NAME = env("SITE_NAME")
SITE_CONTACT_EMAIL = env("SITE_CONTACT_EMAIL")
LEGAL_LAST_UPDATED = env("LEGAL_LAST_UPDATED")
ORIGINAL_RETENTION_DAYS = env("ORIGINAL_RETENTION_DAYS")
RESULT_RETENTION_DAYS = env("RESULT_RETENTION_DAYS")
SESSION_RETENTION_DAYS = env("SESSION_RETENTION_DAYS")

USE_R2 = env("USE_R2")


def _clean_env_string(value):
    return value.strip().strip("'").strip('"').strip("`").strip()


R2_ACCESS_KEY_ID = _clean_env_string(env("R2_ACCESS_KEY_ID", default=""))
R2_SECRET_ACCESS_KEY = _clean_env_string(env("R2_SECRET_ACCESS_KEY", default=""))
R2_BUCKET_NAME = _clean_env_string(env("R2_BUCKET_NAME", default=""))
R2_ENDPOINT_URL = _clean_env_string(env("R2_ENDPOINT_URL", default=""))
R2_PUBLIC_BASE_URL = _clean_env_string(
    env(
        "R2_PUBLIC_BASE_URL",
        default=env("R2_PUBLIC_URL", default=""),
    )
)
R2_SIGNED_URL_TTL = env("R2_SIGNED_URL_TTL")

AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
AWS_S3_ENDPOINT_URL = R2_ENDPOINT_URL
AWS_S3_REGION_NAME = "auto"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_ADDRESSING_STYLE = "path"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = R2_SIGNED_URL_TTL
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True

if USE_R2 and R2_BUCKET_NAME and R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY and R2_ENDPOINT_URL:
    STORAGES = {
        "default": {
            "BACKEND": "project.storage_backends.PrivateR2MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=env("REDIS_URL", default="redis://localhost:6379/0"))
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=CELERY_BROKER_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")

GOOGLE_ANALYTICS_ID = env("GOOGLE_ANALYTICS_ID", default="")

MESSAGE_TAGS = {
    10: "secondary",
    20: "info",
    25: "success",
    30: "warning",
    40: "danger",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
