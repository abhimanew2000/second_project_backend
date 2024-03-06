import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from notification.routing import websocket_urlpatterns as notification_websocket_urlpatterns
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        chat_websocket_urlpatterns + notification_websocket_urlpatterns
    ),
})
