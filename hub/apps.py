from django.apps import AppConfig


class HubConfig(AppConfig):
    name = "hub"

    def ready(self):
        """
        Register the Hub signal receivers when Django starts.
        """
        from .logging_services import signals
