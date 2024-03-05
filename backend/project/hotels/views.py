# accounts/views.py
from rest_framework import generics
from .models import Hotel
from .serializers import HotelSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .models import Room, RoomType, Wishlist
from .serializers import (
    RoomSerializer,
    RoomTypeSerializer,
    HotelsSerializer,
    WishlistSerializer,
)
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import status


class HotelList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer


class RoomTypeList(ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class AutocompleteCityView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "").strip()
        print("Received Query:", repr(query))

        cities = Hotel.objects.filter(
            Q(city__iexact=query) | Q(city__icontains=query)
        ).values_list("city", flat=True)

        print("Filtered Cities:", cities)
        return JsonResponse(list(cities), safe=False)


@require_GET
def get_hotels(request):
    print("hiiii")

    city = request.GET.get("city")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    print("city:", city)
    print("min_price:", min_price)
    print("max_price:", max_price)
    queryset = Hotel.objects.filter(city=city)

    if min_price is not None and max_price is not None:
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        print(queryset, "qqqqqqq")

    serializer = HotelSerializer(queryset, many=True)

    return JsonResponse({"hotels": serializer.data})


@require_GET
def get_hotel_details(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)

    except Hotel.DoesNotExist:
        raise Http404("Hotel does not exist")

    serializer = HotelSerializer(hotel)

    return JsonResponse({"hotel": serializer.data})


def get_hotel_images(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    data = {
        "hotel_image": hotel.image.url.lstrip("/") if hotel.image else None,
        "room_type_images": [
            room_type.image.url.lstrip("/")
            for room_type in hotel.room_types.all()
            if room_type.image
        ],
        "room_images": [
            room.image.url.lstrip("/")  
            for room in hotel.rooms.all()
            if room.image
        ],
    }

    return JsonResponse(data)


class WishlistView(APIView):
    print("entered")
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist is not None:
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response({"hotels": []}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            hotel_id = request.data.get("hotelId")
            print("Received hotel_id:", hotel_id)

            if wishlist.hotels.filter(id=hotel_id).exists():
                return Response(
                    {"error": "Hotel is already in the wishlist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                wishlist.hotels.add(hotel_id)
                serializer = WishlistSerializer(wishlist)
                print(serializer, "SERIALIZER")
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    print("enterred")
    try:
        hotel_id = int(request.data.get("hotel_id"))
        print(hotel_id, "HOTELID")
        hotel = Hotel.objects.get(id=hotel_id)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.hotels.add(hotel)

        return JsonResponse({"success": True, "message": "Hotel added to wishlist."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request):
    try:
        hotel_id = int(request.data.get("hotel_id"))
        hotel = Hotel.objects.get(id=hotel_id)

        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.hotels.remove(hotel)

        return JsonResponse(
            {"success": True, "message": "Hotel removed from wishlist."}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_hotels = wishlist.hotels.all()

        serialized_hotels = [
            {
                "id": hotel.id,
                "name": hotel.name,
                "description": hotel.description,
                "address": hotel.address,
                "image": hotel.image.url,
            }
            for hotel in wishlist_hotels
        ]

        return Response({"hotels": serialized_hotels})
    except Wishlist.DoesNotExist:
        return Response({"hotels": []})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class RoomPricePerNightView(View):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
            price_per_night = room.price_per_night
            return JsonResponse({"price_per_night": price_per_night})
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)


class RoomTypeListByHotel(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RoomTypeSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        roomtypes = RoomType.objects.filter(hotel_id=hotel_id)
        
        # Iterate over each RoomType object to access its price_per_night attribute
        for roomtype in roomtypes:
            print(roomtype.price_per_night)
            print(roomtype)
        
        return roomtypes