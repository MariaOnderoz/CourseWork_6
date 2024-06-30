from time import sleep
from django.apps import AppConfig
from django.core.management import call_command


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

