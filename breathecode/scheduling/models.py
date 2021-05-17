from datetime import timedelta
from django.db import models


MINOR='MINOR'
CRITICAL='CRITICAL'
DONE='DONE'
TASK_RULES_STATUS = (
    (MINOR, 'Minor'),
    (CRITICAL, 'Critical'),
    (DONE, 'Done'),
)
class TaskRules(models.Model):
    slug = models.SlugField(unique=True)

    frequency_delta = models.DurationField(default=timedelta(days=1), help_text='How long to wait for the next execution, defaults to 30 minutes')
    paused_until = models.DateTimeField(null=True, blank=True, default=None, help_text='if you want to stop checking for a period of time')
    last_run = models.DateTimeField(default=None, null=True, blank=True)
    run_once = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    status = models.CharField(max_length=20, choices=TASK_RULES_STATUS, default=DONE)
    status_text = models.CharField(max_length=255, default=None, null=True, blank=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.slug
