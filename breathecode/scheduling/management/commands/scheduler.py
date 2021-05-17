from django.core.management.base import BaseCommand
from ...tasks import task_scheduler


class Command(BaseCommand):
    help = 'Run task scheduler'

    def handle(self, *args, **options):
        task_scheduler.delay()
