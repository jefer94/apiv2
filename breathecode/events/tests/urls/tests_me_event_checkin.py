from datetime import datetime, timedelta, timezone

import capyc.pytest as capy
from django.urls.base import reverse_lazy
from django.utils import timezone


def serialize_event(event):
    return {
        "id": event.id,
        "title": event.title,
        "starting_at": (
            event.starting_at.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
            if isinstance(event.starting_at, datetime)
            else None
        ),
        "ending_at": (
            event.ending_at.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z" if isinstance(event.ending_at, datetime) else None
        ),
        "event_type": {
            "id": event.event_type.id,
            "slug": event.event_type.slug,
            "name": event.event_type.name,
            "technologies": event.event_type.technologies,
        },
        "slug": event.slug,
        "excerpt": event.excerpt,
        "lang": event.lang,
        "url": event.url,
        "banner": event.banner,
        "description": event.description,
        "capacity": event.capacity,
        "status": event.status,
        "host": event.host,
        "ended_at": (event.ended_at.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z" if event.ended_at else None),
        "online_event": event.online_event,
        "is_public": event.is_public,
        "recording_url": event.recording_url,
        "venue": (
            None
            if not event.venue
            else {
                "id": event.venue.id,
                "title": event.venue.title,
                "street_address": event.venue.street_address,
                "city": event.venue.city.name,
                "zip_code": event.venue.zip_code,
                "state": event.venue.state,
                "updated_at": event.venue.updated_at.isoformat(),
            }
        ),
        "academy": (
            None
            if not event.academy
            else {
                "id": event.academy.id,
                "slug": event.academy.slug,
                "name": event.academy.name,
                "city": {"name": event.academy.city.name} if event.academy.city else None,
            }
        ),
        "sync_with_eventbrite": event.sync_with_eventbrite,
        "eventbrite_sync_status": event.eventbrite_sync_status,
        "eventbrite_sync_description": event.eventbrite_sync_description,
        "tags": event.tags,
        "asset_slug": event.asset_slug,
        "host_user": (
            None
            if not event.host_user
            else {
                "id": event.host_user.id,
                "first_name": event.host_user.first_name,
                "last_name": event.host_user.last_name,
                "profile": getattr(event.host_user, "profile", None),
            }
        ),
        "author": (
            None
            if not event.author
            else {
                "id": event.author.id,
                "first_name": event.author.first_name,
                "last_name": event.author.last_name,
            }
        ),
        "asset": None,
    }


def test_filter_by_past_events_of_a_user(client: capy.Client, database: capy.Database, fake: capy.Fake):
    url = reverse_lazy("events:me_event_checkin")

    model = database.create(
        city=1,
        country=1,
        user=1,
        academy={
            "slug": fake.slug(),
            "name": fake.name(),
            "logo_url": "https://example.com/logo.jpg",
            "street_address": "Address",
        },
        event_type=[
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description1",
                "technologies": "python, flask",
            },
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description2",
                "technologies": "flask, pandas",
            },
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description3",
                "technologies": "javascript, java",
            },
        ],
        event={
            "title": "My event",
            "capacity": 100,
            "banner": "https://example.com/banner.jpg",
            "starting_at": timezone.now() - timedelta(hours=2),
            "ending_at": timezone.now(),
            "status": "ACTIVE",
            "event_type_id": 1,
        },
        event_checkin={
            "email": "fake@4geeksacademy.com",
            "attendee": 1,
            "event": 2,
        },
    )
    client.force_authenticate(model.user)
    response = client.get(f"{url}?past=true")
    json = response.json()

    expected = [serialize_event(model.event)]

    assert response.status_code == 200
    assert expected == json


def test_filter_by_future_events_of_a_user(client: capy.Client, database: capy.Database, fake: capy.Fake):
    url = reverse_lazy("events:me_event_checkin")

    model = database.create(
        city=1,
        country=1,
        user=1,
        academy={
            "slug": fake.slug(),
            "name": fake.name(),
            "logo_url": "https://example.com/logo.jpg",
            "street_address": "Address",
        },
        event_type=[
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description1",
                "technologies": "python, flask",
            },
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description2",
                "technologies": "flask, pandas",
            },
            {
                "slug": fake.slug(),
                "name": fake.name(),
                "description": "description3",
                "technologies": "javascript, java",
            },
        ],
        event={
            "title": "My event",
            "capacity": 100,
            "banner": "https://example.com/banner.jpg",
            "starting_at": timezone.now() + timedelta(hours=2),
            "ending_at": timezone.now() + timedelta(hours=6),
            "status": "ACTIVE",
            "event_type_id": 1,
        },
        event_checkin={
            "email": "fake@4geeksacademy.com",
            "attendee": 1,
            "event": 2,
        },
    )
    client.force_authenticate(model.user)
    response = client.get(f"{url}?upcoming=true")
    json = response.json()

    expected = [serialize_event(model.event)]

    assert response.status_code == 200
    assert expected == json
