import logging

logger = logging.getLogger(__name__)

__init__ = ['order_published']


def order_published(self, webhook, payload: dict):
    from breathecode.events.models import Event

    event = Event.objects.filter(eventbrite_id=payload['event_id']).first()
    if not event:
        message = 'event doesn\'t exist'
        logger.error(message)
        raise Exception(message)

    event.status = 'ACTIVE'
    event.eventbrite_status = payload['status']
    event.save()
