from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.messages import error
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from modules.Infrastructure.orm.booking.booking_manage import DjangoBookingRepository, InfoAdapter
from modules.Domain.Services.PaymentBookingService import PaymentService
from modules.Domain.Services.PaymentBookingService import PaymentBookingService
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from modules.Entities.Customer import Customer
from modules.Entities.Booking import Booking, BookingStatus, determine_booking_status
from modules.Entities.Room import Room
from modules.Infrastructure.orm.booking.booking_manage import DjangoBookingRepository
from modules.Infrastructure.orm.db.models import Room as RoomModel
from datetime import date
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
def get_index_view(request):
    """Обработчик для поиска клиента."""
    error_message = None
    customer_data = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()

        try:
            if not name or not surname:
                raise ValidationError("Имя и фамилия обязательны.")

            adapter = InfoAdapter()
            customer_info = adapter.get_customer_info(name, surname)
            print(customer_info)

            request.session["customer_data"] = customer_info

        except (ValidationError, ValueError) as e:
            error_message = str(e)
        except Exception as e:
            error_message = "Внутренняя ошибка сервера."

        if error_message:
            request.session["error_message"] = error_message

    customer_data = request.session.pop("customer_data", None)
    error_message = request.session.pop("error_message", None)

    customer = {
        "customer": customer_data,
        "error": error_message
    }

    template = "index_client.html"
    return render(request, template, customer)

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


def delete_booking(request: HttpRequest):
    if request.method == "POST":
        try:
            # Получаем ID из значения кнопки
            booking_id = int(request.POST.get("delete-booking"))
            repo = DjangoBookingRepository()
            repo.delete(booking_id)
            return redirect("booking_manager")  # Убедитесь, что имя URL 'index' существует
        except ValueError as e:
            # Обработка ошибки (можно добавить сообщение пользователю)
            messages.error(request, str(e))
            return redirect("index")  # Редирект на предыдущую страницу
        except Exception as e:
            messages.error(request, "Произошла ошибка при удалении")
            return redirect("index")
    return HttpResponseNotAllowed(["POST"])


def edit_booking(request: HttpRequest, booking_id: int):
    repo = DjangoBookingRepository()

    if request.method == "GET":
        try:
            booking = repo.get_by_id(booking_id)
            print("Переход на edit:", booking)
            return render(request, 'booking/edit.html', {'booking': booking})
        except Exception as e:
            print("Ошибка при получении бронирования:", str(e))  # Дополнительный вывод
            error(request, f"Произошла ошибка: {str(e)}")
            return redirect('index')

    elif request.method == "POST":
        try:
            print("Полученные данные:", request.POST.dict())
            update_data = {
                'customer_name': request.POST.get('customer_name'),
                'customer_surname': request.POST.get('customer_surname'),
                'room_number': request.POST.get('room_number'),
                'check_in_date': request.POST.get('check_in_date'),
                'check_out_date': request.POST.get('check_out_date'),
                'status': 'waiting',
                'breakfast': 'breakfast' in request.POST,
                'product_intolerance': request.POST.get('product_intolerance')
            }

            repo.update(booking_id, update_data)
            print("Изменения сохранены")
            return redirect('booking_manager')

        except Exception as e:
            messages.error(request, str(e))
            return redirect('edit_booking', booking_id=booking_id)

    return HttpResponseNotAllowed(["GET", "POST"])



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


def booking_list_view(request):
    repository = DjangoBookingRepository()
    bookings = repository.list()
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/booking_manager.html', context)

# @login_required(login_url='/login/')
def index(request):
    return  render(request, "index.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))