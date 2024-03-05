from django.urls import path
from . import consumers
print("check the routing")
websocket_urlpatterns = [
    path('ws/chat/<int:booking_id>/', consumers.AdminUserChatConsumer.as_asgi()),
    
  

]
