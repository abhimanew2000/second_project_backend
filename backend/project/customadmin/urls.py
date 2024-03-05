# accounts/urls.py
from django.urls import path
from .views import (
    AdminLoginView,
    UserListView,
    HotelListView,
    ToggleHotelAvailabilityView,
    HotelUpdateView,
    AdminLogoutView,
    RoomDetailView,
    RoomListView,
    RoomTypeDetailView,
    RoomTypeListView,
    hotel_room_fetch,
    HotelBookingListView,
    CancelBookingView,
    RoomTypeDeleteView,
    SingleHotelDetailView,
    UpdateNotAvailableDates,
    AdminHotelBookingCreateView,
)
from . import views

urlpatterns = [
    # Your existing URLs
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),
    path("user-list/", UserListView.as_view(), name="user-list"),
    path("admin/user/<int:pk>/block/", views.admin_block_user, name="admin-user-block"),
    path(
        "admin/user/<int:pk>/unblock/",
        views.admin_unblock_user,
        name="admin-user-unblock",
    ),
    path("hotel-details/", HotelListView.as_view(), name="hotel_details"),
    path(
        "hotel-details/<int:id>/",
        ToggleHotelAvailabilityView.as_view(),
        name="toggle_hotel_availability",
    ),
    path(
        "hotel-details/<int:pk>/update/", HotelUpdateView.as_view(), name="hotel-update"
    ),
    path("admin-logout/", AdminLogoutView.as_view(), name="admin-logout"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
    path("room-types/", RoomTypeListView.as_view(), name="room-type-list"),
    path("room-types/<int:pk>/", RoomTypeDetailView.as_view(), name="room-type-detail"),
    path("about/<int:hotel_id>/", views.hotel_room_fetch, name="hotel-room-fetch"),
    path(
        "hotel-bookinglist/", HotelBookingListView.as_view(), name="hotel-bookinglist"
    ),
    path(
        "cancel-booking/<int:pk>/", CancelBookingView.as_view(), name="cancel-booking"
    ),
    path(
        "hotel/<int:hotel_id>/room-types/<int:id>/delete/",
        RoomTypeDeleteView.as_view(),
        name="delete-room-type",
    ),
    path(
        "single-hotel-detail/<int:pk>/",
        SingleHotelDetailView.as_view(),
        name="single-hotel-detail",
    ),
    path(
        "update-not-available-dates/<int:hotel_id>/<int:room_id>/",
        UpdateNotAvailableDates.as_view(),
        name="update_not_available_dates",
    ),
    path("bookings/", AdminHotelBookingCreateView.as_view(), name="create_booking"),
]
