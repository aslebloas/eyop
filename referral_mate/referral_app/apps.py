from django.apps import AppConfig


class ReferralAppConfig(AppConfig):
    name = 'referral_app'

    def ready(self):
        from . import signals