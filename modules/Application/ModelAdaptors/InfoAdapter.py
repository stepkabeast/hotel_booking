import sqlite3
from modules.Domain.Models.BookingPreparationInterface import BookingPreparation
from typing import Dict, Any
from modules.Entities.Customer import Customer

class InfoAdapter(BookingPreparation):

    data = None

    def __init__(self, data):
        self.data = data

    def get_customer_info(self, name: str, surname: str) -> Dict[str, Any] | None:
        try:
            conn = sqlite3.connect("db.sqlite3")  # Подключение к базе данных
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM db_customer WHERE name = ? AND surname = ?", (name, surname))
            row = cursor.fetchone()

            conn.close()

            if row:
                # Создаем экземпляр Customer из полученных данных
                customer = Customer(
                    gender=row[1],
                    age=row[2],
                    passport_id=row[3],
                    name=row[4],
                    surname=row[5]
                )
                return {
                    #"id": customer.id,
                    "name": customer.name,
                    "surname": customer.surname,
                    "passport_data": customer.passport_id
                }
            else:
                return None  # Клиент не найден

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None  # Ошибка базы данных