from django.urls import path
from channels.routing import URLRouter

__all__ = ['urlpatterns']

# def include(url, urlconf, namespace):
#     import importlib
#     module = importlib.import_module(urlconf)

#     urlpatterns = getattr(module, 'urlpatterns')
#     return urlpatterns


def include(urlconf):
    import importlib
    module = importlib.import_module(urlconf)

    urlpatterns = getattr(module, 'urlpatterns')
    return urlpatterns


# apps = [
#     ('v1/auth', 'breathecode.authenticate.ws', 'auth'),
# ]

# urlpatterns = [include(url, urlconf, namespace) for url, urlconf, namespace in apps]
urlpatterns = URLRouter(include('breathecode.authenticate.ws'))
