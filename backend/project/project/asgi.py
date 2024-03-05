"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter

# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# django.setup()
# from channels.auth import AuthMiddlewareStack
# from notification.routing import websocket_urlpatterns

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket":AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         )

#     }
# )
# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from notification.routing import websocket_urlpatterns
# from chat.routing import websocket_urlpatterns

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         'websocket': URLRouter(websocket_urlpatterns ),

#     }
# )

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

