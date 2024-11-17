from django.apps import AppConfig


class CeleryBackgroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_background'
