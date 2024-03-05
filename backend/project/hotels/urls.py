# accounts/urls.py
from django.urls import path
from .views import AutocompleteCityView,HotelList,RoomTypeList,WishlistView,RoomPricePerNightView,RoomTypeListByHotel
from django.urls import re_path
from . import views

urlpatterns = [
    path('hotels/', HotelList.as_view(), name='hotel-list'),
    path('roomtypes/', RoomTypeList.as_view(), name='roomtype-list'),
    path('autocomplete_city/', AutocompleteCityView.as_view(), name='autocomplete-city'),
    re_path(r'^get-hotels/$', views.get_hotels, name='get-hotels'),
    path('hotels/about/<int:hotel_id>/', views.get_hotel_details, name='get-hotel-details'),
    path('get-hotel-images/<int:hotel_id>/',views.get_hotel_images, name='get_hotel_images'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('get-wishlist/', views.get_wishlist, name='get_wishlist'),
    path('remove-from-wishlist/',views.remove_from_wishlist, name='remove_from_wishlist'),
    path('room/<int:room_id>/pricepernight/', RoomPricePerNightView.as_view(), name='room-price-per-night'),
    path('<int:hotel_id>/roomtypes/', RoomTypeListByHotel.as_view(), name='roomtypelist'),


]




