#models.py


from django.db import models
from accounts.models import User


# chat/models.py
from django.db import models
from accounts.models import User
from Booking.models import HotelBooking
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='chat_messages', null=True)

    def __str__(self):
        return f'{self.sender} to {self.sender}: {self.message}'









