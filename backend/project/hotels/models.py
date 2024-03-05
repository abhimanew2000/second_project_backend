from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import User

# Create your models here.

class HotelImage(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='multiimage', on_delete=models.CASCADE)
    multiimage = models.ImageField(upload_to='hotel_multi_images/')

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    address = models.TextField()
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)
    availability = models.BooleanField(default=True)
    amenities = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    ratings = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,blank=True,null=True)
    price = models.IntegerField()  
    latitude = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)


    def calculate_average_rating(self):
        feedbacks = Feedback.objects.filter(hotel=self)
        if feedbacks.exists():
            total_ratings = sum(feedback.ratings for feedback in feedbacks)
            average_rating = total_ratings / feedbacks.count()
            return round(average_rating, 2)
        else:
            return 0.0

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.TextField()  
    room_type = models.ForeignKey('RoomType', related_name='rooms', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    rooms = models.ManyToManyField('Room', related_name='hotels', blank=True)


    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"

class RoomType(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='room_type_images/', null=True, blank=True)
    count = models.IntegerField()
    dates = ArrayField(models.DateField(), blank=True, null=True)
    price_per_night = models.IntegerField(null=True, blank=True)


    



    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE) 
    description = models.TextField(blank=True,null=True,max_length =255)
    ratings = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,blank=True,null=True)

    def __str__(self):
        return f"{self.user.name} - {self.hotel.name}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotels = models.ManyToManyField('Hotel')

    def __str__(self):
        return f'Wishlist for {self.user.name}'