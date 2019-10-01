from django.apps import AppConfig


class StableConfig(AppConfig):
    name = 'stable'

    def ready(self):
        import stable.signals
