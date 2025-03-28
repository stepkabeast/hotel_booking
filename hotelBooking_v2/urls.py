from django.contrib import admin
from django.urls import path, include
from booking.views import get_index_view, index, create_booking, booking_success, check_rooms, booking_list_view
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("", include('users.urls')),
    path("info", get_index_view, name="customer_info"),
    path("booking", create_booking, name="create_booking"),
    path("booking/success/<int:booking_id>", booking_success, name="booking-success"),
    path("booking/booking_manager/", booking_list_view, name="booking-manager"),
    path('check_rooms/', check_rooms),
    path('accounts/', include('django.contrib.auth.urls')),
]