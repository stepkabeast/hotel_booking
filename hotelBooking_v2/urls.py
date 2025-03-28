from django.contrib import admin
from django.urls import path, include
from booking.views import get_index_view, index, create_booking, booking_success, check_rooms
urlpatterns = [
    path("admin/", admin.site.urls),
    path("info", get_index_view, name="customer_info"),
    path("index/", index, name="index"),
    path("booking", create_booking, name="create_booking"),
    path("booking/success/<int:booking_id>", booking_success, name="booking-success"),
    path('check_rooms/', check_rooms),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', include('users.urls')),
]