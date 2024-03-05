import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, HotelBooking
from accounts.models import User
from channels.db import database_sync_to_async

class AdminUserChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.booking = await self.get_booking_instance(self.booking_id)

        # Join room group
        await self.channel_layer.group_add(
            f'chat_{self.booking_id}',
            self.channel_name
        )

        await self.accept()
        
        # Fetch existing messages and send them to the connected client
        existing_messages = await self.get_existing_messages()
        for message in existing_messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
                'sender': message['sender'],
                'timestamp': message['timestamp']
            }))

    @database_sync_to_async
    def get_existing_messages(self):
        messages = ChatMessage.objects.filter(booking=self.booking)
    
        x= [{'message': message.message, 'sender': message.sender_id, 'timestamp': message.timestamp.isoformat()} for message in messages]
        print(x)
        return x
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            f'chat_{self.booking_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message') 
        sender_id = data.get('sender')
        timestamp = data.get('timestamp')
        booking_id = data.get('booking')
        
        sender = await self.get_user_instance(sender_id)
        booking = await self.get_booking_instance(booking_id)
        
        if sender and booking:
            await self.save_message(sender, message_content, timestamp, booking)

            # Broadcast message to room group
            await self.channel_layer.group_send(
                f'chat_{self.booking_id}',
                {
                    'type': 'chat.message',
                    'data': {
                        'message': message_content,
                        'sender': sender_id,
                        'timestamp': timestamp
                    }
                }
            )
        else:
            # Handle error when sender or booking is not found
            await self.send(text_data=json.dumps({
                'error': 'Sender or booking not found'
            }))

    async def chat_message(self, event):
        data = event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    @classmethod
    async def send_chat_message(cls, booking_id, message, sender, timestamp):
        await cls.send_group(f'chat_{booking_id}', {
            'type': 'chat.message',
            'data': {
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }
        })

    @database_sync_to_async
    def get_booking_instance(self, booking_id):
        try:
            booking = HotelBooking.objects.get(id=booking_id)
            return booking
        except HotelBooking.DoesNotExist:
            print("Failed to find the booking")

    @database_sync_to_async
    def save_message(self, sender, message_content, timestamp, booking):
        ChatMessage.objects.create(
            message=message_content,
            sender=sender,
            timestamp=timestamp,
            booking=booking
        )

    @database_sync_to_async
    def get_user_instance(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            print("Failed to find the user")