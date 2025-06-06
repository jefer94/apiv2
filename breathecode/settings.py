"""
Django settings for breathecode project.

Generated by 'django-admin startproject' using Django 3.0.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import TypedDict

import dj_database_url
import django_heroku
from django.contrib.messages import constants as messages
from django.utils.log import DEFAULT_LOGGING
from linked_services.core import settings

from breathecode.setup import configure_redis

settings.set_settings(app_name="breathecode")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ.get("DATABASE_URL")
ENVIRONMENT = os.environ.get("ENV")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "5ar3h@ha%y*dc72z=8-ju7@4xqm0o59*@k*c2i=xacmy2r=%4a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == "development" or ENVIRONMENT == "test"


# Application definition
INSTALLED_APPS = [
    "breathecode.admin_styles",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "django.contrib.admindocs",
    "rest_framework",
    "adrf",
    "phonenumber_field",
    "corsheaders",
    "breathecode.activity",
    "breathecode.notify",
    "breathecode.authenticate",
    "breathecode.monitoring",
    "breathecode.admissions",
    "breathecode.events",
    "breathecode.feedback",
    "breathecode.assignments",
    "breathecode.marketing",
    "breathecode.freelance",
    "breathecode.certificate",
    "breathecode.media",
    "breathecode.assessment",
    "breathecode.registry",
    "breathecode.mentorship",
    "breathecode.career",
    "breathecode.commons",
    "breathecode.payments",
    "breathecode.provisioning",
    "breathecode.websocket",
    "explorer",
    "graphene_django",
    "task_manager",
    "linked_services",
]

GRAPHENE = {"SCHEMA": "breathecode.schema.schema"}
IS_TEST_ENV = os.getenv("ENV") == "test"

if os.getenv("ALLOW_UNSAFE_CYPRESS_APP") or ENVIRONMENT == "test":
    INSTALLED_APPS.append("breathecode.cypress")

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "breathecode.utils.HeaderLimitOffsetPagination",
    "EXCEPTION_HANDLER": "capyc.rest_framework.exception_handler.exception_handler",
    "PAGE_SIZE": 100,
    "DEFAULT_VERSION": "v1",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "breathecode.authenticate.authentication.ExpiringTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ),
}

if os.getenv("ENABLE_DEFAULT_PAGINATION", "y") in ["t", "true", "True", "TRUE", "1", "yes", "y"]:
    REST_FRAMEWORK["PAGE_SIZE"] = 20

# whitenoise runs in sync mode, it must be wrapped or removed
# CompressResponseMiddleware must be upgraded because a django deprecation

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "breathecode.middlewares.static_redirect_middleware",
    "breathecode.middlewares.set_service_header_middleware",
    "breathecode.middlewares.detect_pagination_issues_middleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # Cache
    # 'django.middleware.cache.UpdateCacheMiddleware',
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #'breathecode.utils.admin_timezone.TimezoneMiddleware',
    "breathecode.middlewares.CompressResponseMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
]

# if ENVIRONMENT != "test":
#     MIDDLEWARE += ["django_minify_html.middleware.MinifyHtmlMiddleware"]

if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and (GS_BUCKET_NAME := os.getenv("STATIC_BUCKET")):
    from google.oauth2 import service_account

    from .setup import resolve_gcloud_credentials

    resolve_gcloud_credentials()

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    GS_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")
    GS_IS_GZIPPED = True
    GS_QUERYSTRING_AUTH = False
    GS_FILE_OVERWRITE = True
    GZIP_CONTENT_TYPES = (
        "text/html",
        "text/css",
        "text/javascript",
        "application/javascript",
        "application/x-javascript",
        "image/svg+xml",
    )

    # GS_OBJECT_PARAMETERS = {
    #     'cache_control': 'max-age=604800',  # 1 week
    # }

    GS_EXPIRATION = timedelta(days=7)

    STORAGES = {
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        },
    }
    # STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

elif IS_TEST_ENV is False:
    INSTALLED_APPS += [
        "whitenoise.runserver_nostatic",
    ]

    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

DISABLE_SERVER_SIDE_CURSORS = True  # required when using pgbouncer's pool_mode=transaction

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

ROOT_URLCONF = "breathecode.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "breathecode.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Disable Django's logging setup
LOGGING_CONFIG = None

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# this prevent the duplications of logs because heroku redirect the output to Coralogix
if IS_TEST_ENV:
    LOGGING_HANDLERS = ["console"]

else:
    LOGGING_HANDLERS = ["coralogix", "console"]

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                # exact format is not important, this is the minimum information
                "format": "[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "handlers": {
            "coralogix": {
                "class": "coralogix.handlers.CoralogixLogger",
                "formatter": "default",
                "private_key": os.getenv("CORALOGIX_PRIVATE_KEY", ""),
                "app_name": os.getenv("CORALOGIX_APP_NAME", "localhost"),
                "subsystem": os.getenv("CORALOGIX_SUBSYSTEM", "logger"),
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {
                "level": "WARNING",
                "handlers": LOGGING_HANDLERS,
            },
            # Our application code
            "breathecode": {
                "level": LOG_LEVEL,
                "handlers": LOGGING_HANDLERS,
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Prevent noisy modules from logging to Sentry
            "noisy_module": {
                "level": "ERROR",
                "handlers": LOGGING_HANDLERS,
                "propagate": False,
            },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
if "localhost" not in DATABASE_URL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers
ALLOWED_HOSTS = [
    "breathecode.herokuapp.com",
    "breathecode-test.herokuapp.com",
    "localhost",
    "127.0.0.1",
    "*.gitpod.io",
    "*.github.dev",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# static generated automatically
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    # static generated by us
    os.path.join(PROJECT_ROOT, "static"),
]

CSRF_TRUSTED_ORIGINS = [
    "http://*.gitpod.io",
    "https://*.gitpod.io",
    "https://s.4geeksacademy.co",
    "https://s.4geeks.co",
    "https://s.4geeks.com",
    "https://breathecode.herokuapp.com",
    "https://breathecode-test.herokuapp.com",
]

# CSP_DEFAULT_SRC = ("'self'", "https://*.4geeks.com", "https://*.4geeksacademy.co")
# CSP_FRAME_SRC = ("'self'", "https://*.4geeks.com", "https://*.4geeksacademy.co")
# SECURE_REFERRER_POLICY = "no-referrer"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    "accept",
    "academy",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "cache-control",
    "credentials",
    "http-access-control-request-method",
]

# production redis url
REDIS_URL = os.getenv("REDIS_COM_URL", "")
kwargs = {}
IS_REDIS_WITH_SSL_ON_HEROKU = False
IS_REDIS_WITH_SSL = False

# local or heroku redis url
if REDIS_URL == "" or REDIS_URL == "redis://localhost:6379":
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # support for heroku redis addon
    if REDIS_URL.startswith("rediss://"):
        IS_REDIS_WITH_SSL_ON_HEROKU = True

else:
    IS_REDIS_WITH_SSL = True

# on localhost this should be false to avoid SSL Certificate
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "TRUE") == "TRUE"

CACHE_MIDDLEWARE_SECONDS = 60 * int(os.getenv("GLOBAL_CACHE_MINUTES", 60 * 24))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": CACHE_MIDDLEWARE_SECONDS,
    }
}

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

if IS_REDIS_WITH_SSL_ON_HEROKU:
    CACHES["default"]["OPTIONS"] = {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        "PICKLE_VERSION": -1,
        # "IGNORE_EXCEPTIONS": True,
        "CONNECTION_POOL_KWARGS": {
            "ssl_cert_reqs": None,
            "max_connections": int(os.getenv("REDIS_MAX_CONNECTIONS", 500)),
        },
    }
elif IS_REDIS_WITH_SSL:
    redis_ca_cert_path, redis_user_cert_path, redis_user_private_key_path = configure_redis()
    CACHES["default"]["OPTIONS"] = {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        "PICKLE_VERSION": -1,
        # "IGNORE_EXCEPTIONS": True,
        "CONNECTION_POOL_KWARGS": {
            "ssl_cert_reqs": "required",
            "ssl_ca_certs": redis_ca_cert_path,
            "ssl_certfile": redis_user_cert_path,
            "ssl_keyfile": redis_user_private_key_path,
            "max_connections": int(os.getenv("REDIS_MAX_CONNECTIONS", 500)),
        },
    }

if IS_TEST_ENV:
    import fnmatch

    from django.core.cache.backends.locmem import LocMemCache

    class Key(TypedDict):
        key: str
        value: str
        valid_until: datetime

    # TODO: support timeout
    class CustomMemCache(LocMemCache):
        _cache = {}

        fake = 1

        def delete_pattern(self, pattern):
            for key in self._cache.keys():
                if fnmatch.fnmatch(key, pattern):
                    del self._cache[key]

        def delete_many(self, patterns):
            for pattern in patterns:
                self.delete(pattern)

        def delete(self, key, *args, **kwargs):
            if key in self._cache.keys():
                del self._cache[key]

        def keys(self, filter=None):
            if filter:
                return sorted(fnmatch.filter(self._cache.keys(), filter))

            return sorted(self._cache.keys())

        def clear(self):
            self._cache = {}

        # TODO: timeout not implemented yet
        def set(self, key, value, *args, timeout=None, **kwargs):
            if value is None:
                self._cache[key] = None
                return

            self._cache[key] = {
                "key": key,
                "value": value,
                "valid_until": timeout,
            }

        def get(self, key, *args, **kwargs):
            if key not in self._cache.keys():
                return None

            return self._cache[key]["value"]

    CACHES["default"] = {
        **CACHES["default"],
        "LOCATION": "breathecode",
        "BACKEND": "breathecode.settings.CustomMemCache",
    }

# overwrite the redis url with the new one
os.environ["REDIS_URL"] = REDIS_URL

SITE_ID = 1

# Change 'default' database configuration with $DATABASE_URL.
# https://github.com/jacobian/dj-database-url#url-schema
DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=False),
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# SQL Explorer
EXPLORER_CONNECTIONS = {"Default": "default"}
EXPLORER_DEFAULT_CONNECTION = "default"

# Use the format of Django 6.0, remove it when upgrading to Django 6.0
FORMS_URLFIELD_ASSUME_HTTPS = True

sql_keywords_path = Path(os.getcwd()) / "breathecode" / "sql_keywords.json"
with open(sql_keywords_path, "r") as f:
    sql_keywords = json.load(f)

    # https://www.postgresql.org/docs/8.1/sql-keywords-appendix.html
    # scripts/update_sql_keywords_json.py
    # breathecode/sql_keywords.json

    EXPLORER_SQL_BLACKLIST = tuple(sql_keywords["blacklist"])

# Django Rest Hooks
HOOK_EVENTS = {
    # 'any.event.name': 'App.Model.Action' (created/updated/deleted)
    "form_entry.added": "marketing.FormEntry.created+",
    "form_entry.changed": "marketing.FormEntry.updated+",
    "profile_academy.added": "authenticate.ProfileAcademy.created+",
    "profile_academy.changed": "authenticate.ProfileAcademy.updated+",
    "cohort_user.added": "admissions.CohortUser.created+",
    "cohort_user.changed": "admissions.CohortUser.updated+",
    # and custom events, make sure to trigger them at notify.receivers.py
    "cohort_user.edu_status_updated": "admissions.CohortUser.edu_status_updated",
    "cohort.cohort_stage_updated": "admissions.Cohort.cohort_stage_updated",
    "user_invite.invite_status_updated": "authenticate.UserInvite.invite_status_updated",
    "asset.asset_status_updated": "registry.Asset.asset_status_updated",
    "event.event_status_updated": "events.Event.event_status_updated",
    "event.new_event_order": "events.EventCheckin.new_event_order",
    "event.new_event_attendee": "events.EventCheckin.new_event_attendee",
    "form_entry.won_or_lost": "marketing.FormEntry.won_or_lost",
    "form_entry.new_deal": "marketing.FormEntry.new_deal",
    "session.mentorship_session_status": "mentorship.MentorshipSession.mentorship_session_status",
    "planfinancing.planfinancing_created": "payments.PlanFinancing.planfinancing_created",
    "subscription.subscription_created": "payments.Subscription.subscription_created",
    "UserAssessment.userassessment_status_updated": "assessment.UserAssessment.userassessment_status_updated",
}

# Websocket
ASGI_APPLICATION = "breathecode.asgi.application"
REDIS_URL_PATTERN = r"^redis://(.+):(\d+)$"
REDIS_PARTS = REDIS_URL.split(":")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [(":".join(REDIS_PARTS[:-1]), int(REDIS_PARTS[-1]))],
        },
    },
}

heroku_redis_ssl_host = {
    "address": REDIS_URL,  # The 'rediss' schema denotes a SSL connection.
}

if IS_REDIS_WITH_SSL_ON_HEROKU:
    heroku_redis_ssl_host["address"] += "?ssl_cert_reqs=none"


MB = 1024 * 1024

# keeps compatibility with the actual media endpoint
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200 * MB

# keep last part of the file
django_heroku.settings(locals(), databases=False)

# django_heroku does not support the new storages properly required by django 5.0
del locals()["STATICFILES_STORAGE"]
