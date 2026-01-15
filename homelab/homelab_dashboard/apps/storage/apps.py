from django.apps import AppConfig


class StorageConfig(AppConfig):
    """Configuration for the storage app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.storage"
    verbose_name = "Storage Management (NAS)"