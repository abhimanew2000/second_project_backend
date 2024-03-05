from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,RetrieveAPIView
from accounts.models import User
from .serializers import UserSerializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from hotels.models import Hotel
from rest_framework.decorators import api_view, permission_classes
from hotels.serializers import HotelSerializer,HotelsSerializer
from rest_framework.generics import DestroyAPIView
from datetime import datetime

from rest_framework.generics import ListCreateAPIView
import json

from django.http import Http404, JsonResponse
from django.views import View
from hotels .models import Room, RoomType
from hotels.serializers import RoomSerializer, RoomTypeSerializer
from Booking.models import HotelBooking
from Booking.serializers import HotelBookingSerializer
from accounts.views import get_tokens_for_user

class AdminLoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request, format=None):
        email = request.data.get("email")
        print('email',email)
        password = request.data.get("password")
        print('password',password)
        user = authenticate(email=email, password=password)

        if user and user.is_staff:
            token = get_tokens_for_user(user)
            return Response(
                    {"token": token, "msg": "Admin Login Success", "user_email": user.email},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                    {"errors": {"non_field_errors": ["Invalid admin credentials"]}},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class UserListView(ListAPIView):
    permission_classes=[IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializers


@api_view(['PUT'])
def admin_block_user(request, pk):
    print(request.user, 'user')
    print(request.user.id, 'idd')

    user = get_object_or_404(User, id=pk)
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def admin_unblock_user(request, pk):
        user = get_object_or_404(User, id=pk)
        user.is_active = True  
        user.save()
        return Response(status=status.HTTP_200_OK)

class HotelListView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer 


class HotelDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class ToggleHotelAvailabilityView(APIView):
    permission_classes=[IsAdminUser]
    def patch(self, request, id):

        try:
            hotel = Hotel.objects.get(id=id)
            serializer = HotelSerializer(hotel, data={'availability': not hotel.availability}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': f'Toggled availability for hotel with ID: {id}'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Hotel.DoesNotExist:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)




class HotelUpdateView(RetrieveUpdateAPIView):
    permission_classes=[IsAdminUser]
    print("hellooo")

    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer
    lookup_field = 'pk'  
    def put(self, request,*args, **kwargs):
        try:
            instance = self.get_object()  
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.update(request, *args, **kwargs)
            return Response({'success': 'Hotel updated successfully'}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth import logout

class AdminLogoutView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated and request.user.is_superuser:
            logout(request)
            return Response({"msg": "Admin Logout Success"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": {"non_field_errors": ["User is not a superuser or is not authenticated"]}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        




class RoomListView(ListCreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomTypeListView(ListCreateAPIView):
    permission_classes=[IsAdminUser]
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomTypeDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer



class HotelDetailView(RetrieveAPIView):
    permission_classes=[IsAdminUser]
    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer


def hotel_room_fetch(request, hotel_id):
    permission_classes=[IsAdminUser]
    data = {}
    rooms = Room.objects.filter(hotel=hotel_id)
    room_data = []

    for room in rooms:
        room_data.append({
            'room_type': room.room_type.name,
            'price_per_night': room.price_per_night,
            # Add other room fields as needed
        })

    data['rooms'] = room_data
    return JsonResponse(data)


class HotelBookingListView(View):
    permission_classes=[IsAdminUser]
    def get(self, request, *args, **kwargs):
        bookings = HotelBooking.objects.all()
        serialized_bookings = HotelBookingSerializer(bookings, many=True).data
        return JsonResponse({'bookings': serialized_bookings}, safe=False)
    

class CancelBookingView(generics.UpdateAPIView):
    permission_classes=[IsAdminUser]
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_cancelled = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RoomTypeDeleteView(DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'id' 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'success': 'RoomType deleted successfully'}, status=status.HTTP_204_NO_CONTENT)







class SingleHotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.retrieve(request, *args, **kwargs)
    

class UpdateNotAvailableDates(APIView):
    permission_classes = [IsAdminUser]

class UpdateNotAvailableDates(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, hotel_id, room_id):
        try:
            selected_dates = request.data.get('dates', [])

            formatted_dates = []
            for date_str in selected_dates:
                formatted_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                formatted_dates.append(formatted_date)

            room_type = get_object_or_404(RoomType, hotel_id=hotel_id, id=room_id)

            room_type.dates = formatted_dates
            room_type.save()

            return Response({'message': 'Selected dates updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminHotelBookingCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer



