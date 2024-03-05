# serializers.py

from rest_framework import serializers
from .models import HotelBooking
from hotels.serializers import HotelSerializer

class HotelBookingSerializer(serializers.ModelSerializer):
    hotel_details = HotelSerializer(source='hotel', read_only=True)

    class Meta:
        model = HotelBooking
        fields = '__all__'
