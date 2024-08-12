from django.apps import AppConfig
from django.db.models.signals import post_save


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from app import signals
        post_save.connect(signals.run_add_to_vector)
