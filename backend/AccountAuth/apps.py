from django.apps import AppConfig


class AccountauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AccountAuth'

    def ready(self):
        import AccountAuth.signals 