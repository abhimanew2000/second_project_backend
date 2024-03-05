from django.db import models
from accounts.models import User
# Create your models here.

class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



