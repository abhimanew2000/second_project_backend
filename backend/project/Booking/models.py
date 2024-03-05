from django.db import models
from hotels.models import Hotel  
from accounts.models import User
class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)  
    room_type = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    is_main_guest = models.BooleanField(default=True)
    guest_first_name = models.CharField(max_length=255, blank=True, null=True)
    guest_last_name = models.CharField(max_length=255, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=15, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)  
    is_cancelled = models.BooleanField(default=False,blank=True,null=True)
    

    class Meta:
        db_table = 'booking_hotelbooking'


    def __str__(self):
        return f"{self.user.name} - {self.hotel.name} - {self.room_type}"