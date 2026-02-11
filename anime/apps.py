from email.policy import default
from django.apps import AppConfig


class AnimeConfig(AppConfig):
    name = 'anime'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self) -> None:
        import anime.signals
