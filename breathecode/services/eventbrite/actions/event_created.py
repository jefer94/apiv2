import logging

logger = logging.getLogger(__name__)

__init__ = ['event_created']


def event_created(self, webhook, payload: dict):
    # lazyload to fix circular import
    from breathecode.events.models import Organization
    from breathecode.events.actions import update_or_create_event

    org = Organization.objects.filter(id=webhook.organization_id).first()

    update_or_create_event(payload, org)
    webhook.status = 'DONE'
    webhook.status_text = 'OK'

    webhook.save()
