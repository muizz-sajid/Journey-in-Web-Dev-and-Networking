from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts app."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "User Accounts & Authentication"
    
    def ready(self) -> None:
        """
        Perform initialization when app is ready.
        
        This is where you'd import signal handlers, etc.
        """
        # Import signal handlers when they're created
        # import apps.accounts.signals  # noqa
        pass
