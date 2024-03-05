from django.urls import re_path

from . import consumers
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notification/(?P<room_name>\w+)/$", consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/notification/", NotificationConsumer.as_asgi()),

]
