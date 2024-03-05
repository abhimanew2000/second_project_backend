# Booking/urls.py

from django.urls import path
from . import views
from Booking.views import UserBookingListView,UserCancelBookingView
urlpatterns = [
    path('initiate_razorpay_payment/', views.hotel_booking, name='initiate-razorpay-payment'),
    path('confirm_booking/', views.confirm_booking, name='confirm-booking'),
    path('user-booking-list/', UserBookingListView.as_view(), name='user-booking-list'),
    path('cancel/<int:pk>/', UserCancelBookingView.as_view(), name='user-cancel-booking'),
    path('hotel-details/<int:booking_id>/', views.get_hotel_details, name='hotel_details'),


]
