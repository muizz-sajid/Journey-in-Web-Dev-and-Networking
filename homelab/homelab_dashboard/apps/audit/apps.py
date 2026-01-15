from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Configuration for the audit app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    verbose_name = "Audit & Compliance Logging"
    
    def ready(self) -> None:
        """
        Perform initialization when app is ready.
        """
        # Import signal handlers for automatic audit logging
        # import apps.audit.signals  # noqa
        pass
