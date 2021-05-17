from datetime import timedelta
from breathecode.scheduling.actions import list_tasks, run_task
from django.utils import timezone
from time import sleep
from celery import shared_task, Task
from .models import TaskRules
from breathecode.notify.actions import send_email_message, send_slack_raw
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    #                                           seconds
    retry_kwargs = {'max_retries': 5, 'countdown': 60 * 5 }
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def handle_task(self, task_id):
    task = TaskRules.objects.filter(id=task_id).first()

    while True:
        if (task.active and (not self.run_once or
                (self.run_once and not task.last_run))):
            run_task(task)

        sleep(task.frequency_delta.total_seconds())
        task = TaskRules.objects.filter(id=task_id).first()


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_scheduler(self):
    list_task_slugs = list_tasks()
    for slug in list_task_slugs:
        if not TaskRules.objects.filter(slug=slug).exists():
            TaskRules(slug=slug).save()

    for id, slug in TaskRules.objects.filter().values_list('id', 'slug'):
        if not slug in list_task_slugs:
            TaskRules.objects.filter(slug=slug).delete()
            continue

        handle_task.delay(id)
