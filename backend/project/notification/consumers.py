import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Notification
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Entered')
        self.room_group_name = "notification_group"
        # Join global notification group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.fetch_and_send_notifications()


    async def disconnect(self, close_code):
        print('disconnected')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        if message:
            print(message, "received message")
            await self.save_notification(message)
            await self.send_notification_message(message)
        else:
            print("Received message does not contain 'message' key",text_data)

    @database_sync_to_async
    def save_notification(self, message):
        Notification.objects.create(message=message)

    async def send_notification_message(self, message):
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def fetch_and_send_notifications(self):
        notifications = await self.get_notifications_from_database()
        await self.send(text_data=json.dumps({
            'notifications': notifications
        }))

    @database_sync_to_async
    def get_notifications_from_database(self):
        notifications = list(Notification.objects.all().values_list('message', flat=True))
        return notifications