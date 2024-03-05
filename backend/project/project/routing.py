# from channels.routing import ProtocolTypeRouter, URLRouter
# from notification.routing import websocket_urlpatterns
# application = ProtocolTypeRouter(
#     {
#         "websocket": URLRouter(websocket_urlpatterns),
      
#     }
# )
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from notification.routing import websocket_urlpatterns as notification_websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        chat_websocket_urlpatterns + notification_websocket_urlpatterns
    ),
})

