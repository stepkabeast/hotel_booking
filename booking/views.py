from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from modules.Infrastructure.orm.booking.booking_manage import DjangoBookingRepository, InfoAdapter
from modules.Domain.Services.PaymentBookingService import PaymentService
from modules.Domain.Services.PaymentBookingService import PaymentBookingService
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from modules.Entities.Customer import Customer
from modules.Entities.Booking import Booking, BookingStatus, determine_booking_status
from modules.Entities.Room import Room
from modules.Infrastructure.orm.booking.booking_manage import DjangoBookingRepository
from modules.Infrastructure.orm.db.models import Room as RoomModel
from datetime import date
def get_index_view(request):
    """Обработчик для поиска клиента."""
    error_message = None
    customer_data = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()

        try:
            # Валидация входных данных
            if not name or not surname:
                raise ValidationError("Имя и фамилия обязательны.")

            # Поиск клиента через адаптер
            adapter = InfoAdapter()
            customer_info = adapter.get_customer_info(name, surname)

            # Сохранение данных в сессии
            request.session["customer_data"] = customer_info

        except (ValidationError, ValueError) as e:
            error_message = str(e)
        except Exception as e:
            error_message = "Внутренняя ошибка сервера."

        # Сохранение ошибки
        if error_message:
            request.session["error_message"] = error_message

        # GET-запрос: извлечение данных из сессии
        customer_data = request.session.pop("customer_data", None)
        error_message = request.session.pop("error_message", None)

        context = {
            "customer": customer_data,
            "error": error_message
        }

        # Выбор шаблона
        template = "index_client.html"
        return render(request, template, context)
    else:
        template = "client_info.html"
        return render(request, template)

def create_booking(request: HttpRequest):
    if request.method == "POST":
        try:
            # Парсим данные клиента
            customer_data = {
                "name": request.POST["name"],
                "surname": request.POST["surname"],
                "age": int(request.POST["age"]),
                "passport_id": _parse_passport(request.POST["passport"]),
                "gender": request.POST["gender"]
            }

            # Парсим данные комнаты
            room_data = {
                "number": request.POST["room_number"],
                "category": request.POST["room_category"]
            }

            # Парсим даты
            check_in_str = request.POST.get("check_in_date")
            check_out_str = request.POST.get("check_out_date")

            check_in = date.fromisoformat(check_in_str)
            check_out = date.fromisoformat(check_out_str)

            # Определяем статус бронирования
            status = determine_booking_status(check_in, check_out)

            # Формируем данные для создания бронирования
            booking_data = {
                "customer": customer_data,
                "room": room_data,
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "status": status.value,  # Преобразуем Enum в строку
                "breakfast": "breakfast" in request.POST,
                "product_intolerance": []  # Можно добавить логику для этого поля
            }

            # Создаем бронирование через репозиторий
            repo = DjangoBookingRepository()
            booking_id = repo.create(booking_data)

            return redirect("booking-success", booking_id=booking_id)

        except Exception as e:
            return render(request, "booking/create_booking.html", {
                "error": str(e),
                "form_data": request.POST
            })

    return render(request, "booking/create_booking.html")


def _parse_customer_data(post_data) -> Customer:
    """Создает и валидирует объект Customer"""
    passport = _parse_passport(post_data.get("passport", ""))

    customer = Customer(
        name=post_data["name"],
        surname=post_data["surname"],
        age=int(post_data["age"]),
        passport_id=passport,
        gender=post_data["gender"]
    )

    if not customer.is_valid():
        raise ValueError("Некорректные данные клиента")

    return customer


def _get_room(number: str, category: str) -> Room:
    try:
        # Используем filter вместо get
        rooms = RoomModel.objects.filter(number=number, category=category)

        if not rooms:
            raise ValueError(f"Комната {category} №{number} не найдена")

        if len(rooms) > 1:
            raise ValueError(f"Найдено несколько комнат {category} №{number}")

        return Room(
            category=rooms[0].category,
            number=rooms[0].number
        )

    except Exception as e:
        raise ValueError(f"Ошибка при поиске комнаты: {str(e)}")


def _parse_passport(passport_str: str) -> dict:
    """Парсим паспортные данные"""
    try:
        series, number = passport_str.split()
        if len(series) != 4 or len(number) != 6:
            raise ValueError
        return {"series": series, "number": number}
    except:
        raise ValueError("Неверный формат паспорта. Пример: 1234 567890")


def booking_success(request, booking_id):
    return render(request, "booking/success.html", {
        "booking_id": booking_id
    })



@csrf_exempt
def check_rooms(request):
    if request.method == 'GET':
        try:
            category = request.GET.get('category')
            if not category:
                return JsonResponse({"error": "Category parameter is required."}, status=400)
            adapter = InfoAdapter()
            bookings = adapter.check_rooms(category)
            print(category)
            print(bookings)
            return JsonResponse(list(bookings), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed."}, status=405)


def index(request):
    return  render(request, "index.html")