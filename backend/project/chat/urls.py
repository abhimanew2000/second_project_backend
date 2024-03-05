from django.urls import path
from . import views


urlpatterns = [
    path('messages/', views.get_all_chat_messages, name='all_chat_messages'),
    path('hotel-details/<int:booking_id>/', views.hotel_details_view, name='hotel_details'),


]

