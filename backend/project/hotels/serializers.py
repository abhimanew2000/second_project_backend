# hotels/serializers.py
from rest_framework import serializers
from .models import Hotel,Room,RoomType,Feedback,Wishlist

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    
   
    


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
    

class HotelsSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True,)
    class Meta:
        model = Hotel
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }

class HotelWithAverageRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'ratings', 'price', 'city', 'image', 'amenities', 'average_rating']

    def get_average_rating(self, obj):
        return obj.calculate_average_rating()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user', 'hotel', 'description', 'ratings']


class WishlistSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'