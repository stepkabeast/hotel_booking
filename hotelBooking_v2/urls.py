"""
URL configuration for hotelBooking_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from booking.views import get_index_view, index, create_booking
urlpatterns = [
    path("admin/", admin.site.urls),
    path("info", get_index_view, name="customer_info"),
    #path("/info", get_index_view, name="index"), # Изменено имя маршрута
    path("", index, name="index"),
    path("booking", create_booking, name="create_booking"),

]
