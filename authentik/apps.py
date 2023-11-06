from django.apps import AppConfig


class AuthentikConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentik'

    def ready(self):
        import authentik.signals