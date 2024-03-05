from django.http import JsonResponse
from .models import ChatMessage
from Booking.models import HotelBooking
def get_all_chat_messages(request):
    # Fetch all chat messages along with sender's name
    messages = ChatMessage.objects.select_related('sender').values(
        'id',
        'message',
        'timestamp',
        'booking_id',
        'sender__name'  
    )
    return JsonResponse(list(messages), safe=False)


def hotel_details_view(request, booking_id):
    try:
        booking = HotelBooking.objects.get(id=booking_id)
        hotel_details = {
            'name': booking.hotel.name,
            'description': booking.hotel.description,
            'city': booking.hotel.city,
            'address': booking.hotel.address,
            'image': booking.hotel.image.url if booking.hotel.image else None,
            # Include other fields as needed
        }
        return JsonResponse(hotel_details)
    except HotelBooking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    


