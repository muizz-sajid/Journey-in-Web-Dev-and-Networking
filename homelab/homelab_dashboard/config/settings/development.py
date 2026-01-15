"""
Development settings for Homelab Dashboard.

Overrides base.py with development-specific configuration.
Prioritizes developer experience and debugging over security.

NEVER use these settings in production.
"""

from .base import *  # noqa: F403, F401


# Debug mode
DEBUG = True

# Allowed hosts (permissive in development)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "[::1]"]

# Database - SQLite is fine for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        "ATOMIC_REQUESTS": True,
    }
}


# Session and cookie security (relaxed for local development)
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400  # 24 hours
CSRF_COOKIE_SECURE = False


# Email backend (console output)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Static and media files
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405


# Logging
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "DEBUG"  # noqa: F405


# Create logs directory if it doesn't exist
import os
os.makedirs(BASE_DIR / "logs", exist_ok=True)  # noqa: F405


# DRF Browsable API
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]


# Mock mode for external services
STORAGE_MOCK_MODE = True
MEDIA_MOCK_MODE = True

# Development-specific flags
ENABLE_SILK_PROFILING = False  # Set to True if/when django-silk installed
ENABLE_QUERY_DEBUGGING = True



print("Development settings loaded")
print(f"Database: {DATABASES['default']['NAME']}")  # noqa: F405
print(f"Debug mode: {DEBUG}")