"""
dharmzeey — production settings.

Usage:
    DJANGO_SETTINGS_MODULE=core.settings.prod gunicorn core.wsgi
"""
from .base import *  # noqa: F401, F403
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'


# ── Database — PostgreSQL ─────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":     os.environ["DB_NAME"],
        "USER":     os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST":     os.environ.get("DB_HOST", "localhost"),
        "PORT":     os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# ── Media storage — Backblaze B2 (S3-compatible) ──────────────────────────────
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}


AWS_ACCESS_KEY_ID = os.environ.get('B2_APPLICATION_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('B2_APPLICATION_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('B2_REALM', 'eu-central-003')
AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.backblazeb2.com'

# AWS_S3_CUSTOM_DOMAIN = "media.dharmzeey.com"
# AWS_LOCATION = "media"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"


STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/staticfiles'

# # ---------------------------------------------------------------------------
# # Security hardening
# # ---------------------------------------------------------------------------
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = "DENY"
# SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# CSRF_TRUSTED_ORIGINS = [
#     o for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o
# ]

# # ---------------------------------------------------------------------------
# # Logging
# # ---------------------------------------------------------------------------
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "INFO",
#     },
#     "loggers": {
#         "django.request": {
#             "handlers": ["console"],
#             "level": "WARNING",
#             "propagate": False,
#         },
#     },
# }
