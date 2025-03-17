from django.shortcuts import render, redirect

from modules.Infrastructure.orm.booking.booking_manage import BookingManager, InfoAdapter
from modules.Domain.Services.PaymentBookingService import PaymentService
from modules.Domain.Services.PaymentBookingService import PaymentBookingService

def get_index_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")

        if name and surname:
            adapter = InfoAdapter(data=None)
            index = adapter.get_customer_info(name, surname)

            if index:
                request.session["customer_data"] = index
                return redirect("index")
            else:
                request.session["error_message"] = "Клиент не найден"  # Сохраняем сообщение об ошибке в сессии
                return redirect("index")
        else:
            request.session["error_message"] = "Введите имя и фамилию"
            return redirect("index")

    customer_data = request.session.pop("customer_data", None)
    error_message = request.session.pop("error_message", None)  # Извлекаем сообщение об ошибке из сессии

    if customer_data:
        return render(request, "index_client.html", {"customer": customer_data})

    return render(request, "client_info.html", {"error": error_message})  # Передаем сообщение об ошибке в шаблон

def create_booking(request):
    if request.method == "POST":
        pass
    return render(request, template_name="booking/create_booking.html")

def index(request):
    return  render(request, "index.html")