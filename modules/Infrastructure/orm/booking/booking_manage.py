import sqlite3

from modules.Application.ModelAdaptors.InfoAdapter import BookingRepository
from modules.Domain.Models.BookingPreparationInterface import BookingPreparation
from typing import Dict, Any, Optional, List
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

class BookingManager(BookingRepository):
    def __init__(self, db_path: str, table_name: str):
        self.db_path = db_path
        self.table_name = table_name
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create(self, data: Dict[str, Any]) -> int:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        set_values = ", ".join([f"{key} = ?" for key in data.keys()])
        values = tuple(list(data.values()) + [id])

        query = f"UPDATE {self.table_name} SET {set_values} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        if filters:
            conditions = " AND ".join([f"{key} = ?" for key in filters.keys()])
            query += f" WHERE {conditions}"
            values = tuple(filters.values())
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def __del__(self):
        self.conn.close()
