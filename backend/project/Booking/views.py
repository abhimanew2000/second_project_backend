from django.shortcuts import render
import razorpay
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import HotelBooking
from django.db import transaction
from.serializers import HotelBookingSerializer
from hotels.models import Hotel
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Value, BooleanField
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from hotels.models import RoomType
from django.shortcuts import get_object_or_404






@csrf_exempt
def hotel_booking(request):
    permission_classes=[IsAuthenticated]
    print(request.method)  
    if request.method == 'POST':
        print("hii")
        try:
            data = json.loads(request.body.decode('utf-8'))
            total_price = data.get('totalPrice')
            room_type = data.get('roomType')  
            hotelId = data.get('hotelId')  # Include roomType in the request

            print("Received Room Type:", room_type)
            print("Received Total Price:", total_price)

            print(total_price, "totalprice")

            razorpay_key = "rzp_test_4o90y50Nv7s1jR"
            razorpay_secret = "nlmYaIYmAyx29rc3BUZSmDRu"
            
            client = razorpay.Client(auth=(razorpay_key, razorpay_secret))

            order_amount = int(float(total_price) * 100)
            order_currency = "INR"
            order_receipt = "order_rcptid_11" 

            response = client.order.create(
                data={
                    'amount': order_amount,
                    'currency': order_currency,
                    'receipt': order_receipt,
                }
            )

            # Pass the order details to the frontend
            context = {
                "order_id": response["id"],
                "order_amount": order_amount,
                "order_currency": order_currency,
                "order_receipt": order_receipt,
                "razorpay_key": razorpay_key,  
            }
            return JsonResponse(context)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'status': 'failure', 'reason': str(e)})
    else:
        return JsonResponse({'status': 'failure', 'reason': 'Invalid request method'})

@csrf_exempt
def confirm_booking(request):
    permission_classes=[IsAuthenticated]
    print("entered")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data, 'data')
        razorpay_signature = data.get('razorpaySignature')
        print(razorpay_signature, 'signature')
        razorpay_payment_id = data.get('razorpayPaymentId')
        print(razorpay_payment_id, 'payment_id')    
        user_name = data.get('email', '')
        try:
            user = User.objects.get(email=user_name)
            print(user,'userrrrr')
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'failure', 'reason': 'User not found'})
        hotel_id = data.get('hotel', '')
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'failure', 'reason': 'Hotel not found'})
        room_type_name=data.get('roomType', '')
        print(room_type_name,'roomtype')
        total_price=data.get('totalPrice', '')
        print(total_price,'totalprice')
        check_in_date=data.get('checkInDate', '')
        print(check_in_date,'checkint')
        check_out_date=data.get('checkOutDate', '')
        print(check_out_date,'checkout')
        is_main_guest=data.get('isMainGuest', False)
        print(is_main_guest,'gurst')
        guest_first_name=data.get('firstName', '')
        print(guest_first_name,'firstname')
        guest_last_name=data.get('lastName', '')
        print(guest_last_name)
        guest_email=data.get('email', ''),
        guest_phone=data.get('phone', ''),
        razorpay_order_id=data.get('razorpay_order_id', ''),
        razorpay_signature=razorpay_signature,
        razorpay_payment_id=razorpay_payment_id,

        try:
            razorpay_key = "rzp_test_4o90y50Nv7s1jR"
            razorpay_secret = "nlmYaIYmAyx29rc3BUZSmDRu"
            # Verify Razorpay signature
            client = razorpay.Client(api_key=razorpay_key, api_secret=razorpay_secret)
            params_dict = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            print(params_dict,'dict')

            room_type = RoomType.objects.get(hotel=hotel,name=room_type_name)
            if room_type.count>0:
                room_type.count -=1
                room_type.save()
            else:
                return JsonResponse({'status':'failure','reason':'No available rooms of this Type'})
            booking =HotelBooking.objects.create(
                    user=user,
                    hotel=hotel,
                    room_type=data.get('roomType', ''),
                    total_price=data.get('totalPrice', ''),
                    check_in_date=data.get('checkInDate', ''),
                    check_out_date=data.get('checkOutDate', ''),
                    is_main_guest=data.get('isMainGuest', False),
                    guest_first_name=data.get('firstName', ''),
                    guest_last_name=data.get('lastName', ''),
                    guest_email=data.get('email', ''),
                    guest_phone=data.get('phone', ''),
                    razorpay_order_id=razorpay_payment_id,
                    
                )
            serializer=HotelBookingSerializer(data=booking)
            if serializer.is_valid():
                booking=serializer.save()

            return JsonResponse({'status': 'success', 'message': 'Booking confirmed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'reason': str(e)})
    return JsonResponse({'status': 'failure', 'reason': 'Invalid request method'})





# ------------------------------------------------------------------------
class UserBookingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelBookingSerializer

    def get_queryset(self):
        user = self.request.user
        return HotelBooking.objects.filter(user=user).select_related('hotel').order_by('is_cancelled')



# ------------------------------------
class UserCancelBookingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_cancelled = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@permission_classes([AllowAny])
def get_hotel_details(request, booking_id):
    booking = get_object_or_404(HotelBooking, pk=booking_id)
    hotel = booking.hotel

    # Serialize hotel data as needed
    serialized_hotel = {
        'name': hotel.name,
        'description': hotel.description,
        'city': hotel.city,
        'address': hotel.address,
        'image': str(hotel.image),  # Convert ImageField to string for URL
        'availability': hotel.availability,
        'amenities': hotel.amenities,
        'ratings': str(hotel.ratings),  # Convert DecimalField to string
        'price': hotel.price,
        'latitude': str(hotel.latitude),  # Convert DecimalField to string
        'longitude': str(hotel.longitude),  # Convert DecimalField to string
    }

    return JsonResponse({'hotel': serialized_hotel})