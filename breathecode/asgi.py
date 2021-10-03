import os
import django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .ws import urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathecode.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    # "websocket": AuthMiddlewareStack(urlpatterns),
    'websocket': urlpatterns,
})
