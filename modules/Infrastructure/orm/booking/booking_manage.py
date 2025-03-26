from typing import Dict, Any, List
from modules.Domain.Models.BookingPreparationInterface import BookingPreparation
from django.core.exceptions import ObjectDoesNotExist
from modules.Infrastructure.orm.db.models import Booking as BookingModel, Customer as CustomerModel, Room as RoomModel
from modules.Application.ModelAdaptors.InfoAdapter import BookingRepository
from django.db.models import Q

class InfoAdapter(BookingPreparation):
    """Адаптер для проверки предварительной информации для бронирования."""

    def get_customer_info(self, name: str, surname: str) -> Dict[str, Any]:
        try:
            customer = CustomerModel.objects.get(name=name, surname=surname)
            return {
                "id": customer.id,
                "name": customer.name,
                "surname": customer.surname,
                "age": customer.age,
                "passport": customer.passport_id,
                "gender": customer.gender
            }
        except ObjectDoesNotExist:
            raise ValueError("Клиент не найден")
        except Exception as e:
            raise ValueError(f"Ошибка базы данных: {str(e)}")

    def check_rooms(self)->List[int]:
        try:
            bookings = BookingModel.objects.filter(status='evicted').values_list('room_id', flat=True)
            return bookings
        except ObjectDoesNotExist:
            raise ValueError("Не удалось получить список свободных номеров")


class DjangoBookingRepository(BookingRepository):
    """
    Реализация репозитория для работы с Django ORM.
    """

    def create(self, data: Dict[str, Any]) -> int:
        try:
            # Сохраняем или обновляем клиента
            customer_data = data["customer"]
            customer, _ = CustomerModel.objects.update_or_create(
                passport_id=customer_data["passport_id"],
                defaults={
                    "name": customer_data["name"],
                    "surname": customer_data["surname"],
                    "age": customer_data["age"],
                    "gender": customer_data["gender"]
                }
            )

            # Получаем комнату
            room_data = data["room"]
            room = RoomModel.objects.get(
                number=room_data["number"],
                category=room_data["category"]
            )

            # Создаем бронирование
            booking = BookingModel.objects.create(
                customer=customer,
                room=room,
                check_in_date=data["check_in_date"],
                check_out_date=data["check_out_date"],
                status=data["status"],
                breakfast=data["breakfast"],
                product_intolerance=data.get("product_intolerance", [])
            )

            return booking.id

        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле: {str(e)}")
        except ObjectDoesNotExist:
            raise ValueError("Комната не найдена")
        except Exception as e:
            raise ValueError(f"Ошибка при создании бронирования: {str(e)}")