from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # for work with signals
    def ready(self):
        import accounts.signals
