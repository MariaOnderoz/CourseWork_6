from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BlockingScheduler
from mailing.services import send_mailing


class Command(BaseCommand):
    help = 'Starts the scheduled mailings'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(send_mailing, 'interval', seconds=60)
        scheduler.start()

