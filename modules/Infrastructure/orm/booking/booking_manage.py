from typing import Dict, Any
from modules.Domain.Models.BookingPreparationInterface import BookingPreparation
from django.core.exceptions import ObjectDoesNotExist
from modules.Infrastructure.orm.db.models import Booking as BookingModel, Customer as CustomerModel, Room as RoomModel
from modules.Application.ModelAdaptors.InfoAdapter import BookingRepository
import sqlite3


class InfoAdapter(BookingPreparation):
    """Адаптер для работы с данными клиента."""

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


class DjangoBookingRepository(BookingRepository):
    """
    Реализация репозитория для работы с Django ORM.
    """

    def create(self, data: Dict[str, Any]) -> int:
        """
        Создает новую запись бронирования в базе данных.

        Args:
            data: Словарь с данными для создания бронирования. Ожидаемые ключи:
                - customer: Dict[str, Any] (данные клиента)
                - room: Dict[str, Any] (данные комнаты)
                - check_in_date: str (дата заезда)
                - check_out_date: str (дата выезда)
                - status: str (статус бронирования)
                - breakfast: bool (включен ли завтрак)
                - product_intolerance: List[str] (список непереносимостей)

        Returns:
            int: Идентификатор созданной записи бронирования.

        Raises:
            ValueError: Если данные некорректны или комната не найдена.
        """
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