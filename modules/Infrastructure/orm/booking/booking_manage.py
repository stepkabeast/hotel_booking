import traceback
from typing import Dict, Any, List, Optional
from modules.Domain.Models.BookingPreparationInterface import BookingPreparation
from django.core.exceptions import ObjectDoesNotExist
from modules.Infrastructure.orm.db.models import Booking as BookingModel, Customer as CustomerModel, Room as RoomModel
from modules.Application.ModelAdaptors.InfoAdapter import BookingRepository
from django.db.models import Q, F, Prefetch


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
                "passport": f"{customer.passport_id["series"]} / {customer.passport_id["number"]}",
                "gender": customer.gender
            }
        except ObjectDoesNotExist:
            raise ValueError("Клиент не найден")
        except Exception as e:
            raise ValueError(f"Ошибка базы данных: {str(e)}")

    def check_rooms(self, category:str)->List[int]:
        try:
            bookings = BookingModel.objects.filter(
                status='waiting',
                room__category=category,
            ).annotate(
                room_category=F('room__category'),
                room_number = F('room__number')
            ).values(
                'id', 'check_in_date', 'check_out_date', 'room_id', 'customer_id',
                'breakfast', 'product_intolerance', 'status', 'room_category', 'room_number'
            )
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

    def get_by_id(self, booking_id: int) -> BookingModel:
        try:
            return BookingModel.objects.get(id=booking_id)
        except BookingModel.DoesNotExist:
            raise ValueError("Бронирование не найдено")

    def delete(self, booking_id: int) -> bool:
        try:
            booking = BookingModel.objects.get(id=booking_id)  # Используйте get вместо filter
            booking.delete()
            return True
        except BookingModel.DoesNotExist:  # Конкретное исключение
            raise ValueError("Бронирование не найдено")

    def update(self, booking_id: int, update_data: dict) -> BookingModel:
        try:
            booking = BookingModel.objects.get(id=booking_id)
            print("Нашли объект:", booking)
            for field, value in update_data.items():
                setattr(booking, field, value)
                print(f"Установлено значение {field}: {value}")
            booking.save()
            print("Запись успешно сохранена.")
            return booking
        except BookingModel.DoesNotExist:
            print("Объект не найден!")
            raise ValueError("Бронь не найдена.")
        except Exception as e:
            print("Ошибка при обновлении:", str(e))
            traceback.print_exc()
            raise RuntimeError(f"Ошибка обновления: {str(e)}")


    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        queryset = BookingModel.objects.all().select_related('customer', 'room').prefetch_related(
            Prefetch('customer', queryset=CustomerModel.objects.only('name', 'surname')),
            Prefetch('room', queryset=RoomModel.objects.only('number', 'category'))
        )

        if filters:
            conditions = []

            # Фильтрация по клиенту
            if 'customer' in filters:
                conditions.append(Q(customer__id=filters['customer']))

            # Фильтрация по номеру комнаты
            if 'room' in filters:
                conditions.append(Q(room__id=filters['room']))

            # Фильтрация по дате заселения
            if 'check_in_date' in filters:
                conditions.append(Q(check_in_date__gte=filters['check_in_date']))

            # Фильтрация по дате выселения
            if 'check_out_date' in filters:
                conditions.append(Q(check_out_date__lte=filters['check_out_date']))

            # Фильтрация по статусу бронирования
            if 'status' in filters:
                conditions.append(Q(status=filters['status']))

            # Применение условий фильтрации
            if conditions:
                queryset = queryset.filter(*conditions)

        # Преобразование QuerySet в список словарей
        bookings = list(queryset.values(
            'id', 'check_in_date', 'check_out_date', 'status', 'breakfast', 'product_intolerance',
            customer_name=F('customer__name'),
            customer_surname=F('customer__surname'),
            room_number=F('room__number'),
            room_category=F('room__category')
        ))

        return bookings