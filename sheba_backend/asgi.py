"""
ASGI config for sheba_backend project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
