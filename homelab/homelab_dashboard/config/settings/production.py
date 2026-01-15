"""
Production settings for Homelab Dashboard.

Overrides base.py with production-hardened configuration.
Prioritizes security and performance over developer convenience.

Environment variables are REQUIRED for production deployment.
"""

from .base import *  # noqa: F403, F401


# Debug mode must be False in production
DEBUG = False

# Allowed hosts must be explicitly set
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())  # noqa: F405

if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set in production")



# Security settings
SECRET_KEY = config("SECRET_KEY")  # noqa: F405

if SECRET_KEY == "INSECURE-change-this-in-production-use-strong-random-key":
    raise ValueError("SECRET_KEY must be changed in production")


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),  # noqa: F405
        "USER": config("DB_USER"),  # noqa: F405
        "PASSWORD": config("DB_PASSWORD"),  # noqa: F405
        "HOST": config("DB_HOST", default="localhost"),  # noqa: F405
        "PORT": config("DB_PORT", default="5432"),  # noqa: F405
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=600, cast=int),  # noqa: F405
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}



# Session and cookie security (HTTPS enforced)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=3600, cast=int)  # noqa: F405

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"



# HTTPS/SSL settings
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)  # noqa: F405
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# HSTS (HTTP Strict Transport Security)
# Gonna keep it disabled for now cuz it seems too permanent for my usecase
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=3600, cast=int)  # noqa: F405, 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool)  # noqa: F405

# Especially this- (Pls future me, DO NOT enable this unless you are ABSOLUTELY sure you want to)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)  # noqa: F405



# Email configuration (proabably not gonna use this)
'''
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="localhost")  # noqa: F405
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)  # noqa: F405
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)  # noqa: F405
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@homelab.local")  # noqa: F405
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Admin notifications
ADMINS = [
    ("Admin", config("ADMIN_EMAIL", default="admin@homelab.local")),  # noqa: F405
]
MANAGERS = ADMINS

'''


# Static files - use WhiteNoise or CDN in production
STATIC_ROOT = config("STATIC_ROOT", default=str(BASE_DIR / "staticfiles"))  # noqa: F405
MEDIA_ROOT = config("MEDIA_ROOT", default=str(BASE_DIR / "media"))  # noqa: F405



# Send error emails to admins
LOGGING["handlers"]["mail_admins"] = {  # noqa: F405
    "level": "ERROR",
    "class": "django.utils.log.AdminEmailHandler",
    "include_html": True,
}
LOGGING["loggers"]["django.request"]["handlers"] = ["console", "file", "mail_admins"]  # noqa: F405

# DRF - production optimizations
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    # Disable browsable API in production
]

# Stricter throttling in production
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {  # noqa: F405
    "anon": config("THROTTLE_ANON", default="50/hour"),  # noqa: F405
    "user": config("THROTTLE_USER", default="500/hour"),  # noqa: F405
}



# Production-specific flags
STORAGE_MOCK_MODE = config("STORAGE_MOCK_MODE", default=False, cast=bool)  # noqa: F405
MEDIA_MOCK_MODE = config("MEDIA_MOCK_MODE", default=False, cast=bool)  # noqa: F405

# Audit log retention
AUDIT_LOG_RETENTION_DAYS = config("AUDIT_LOG_RETENTION_DAYS", default=90, cast=int)  # noqa: F405

# Ensure critical directories exist
import os
os.makedirs(STATIC_ROOT, exist_ok=True)  # noqa: F405
os.makedirs(MEDIA_ROOT, exist_ok=True)  # noqa: F405
os.makedirs(BASE_DIR / "logs", exist_ok=True)  # noqa: F405



print("Production settings loaded")
print(f"HTTPS Redirect: {SECURE_SSL_REDIRECT}")
print(f"HSTS Enabled: {SECURE_HSTS_SECONDS > 0}")
print(f"Database: PostgreSQL at {DATABASES['default']['HOST']}")  # noqa: F405