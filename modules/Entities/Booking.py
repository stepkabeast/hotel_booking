from enum import Enum
from datetime import date
from typing import Dict, Any


class BookingStatus(str, Enum):
    WAITING = 'waiting'
    SETTLED = 'settled'
    EXTENDED = 'extended'
    EVICTED = 'evicted'


def determine_booking_status(check_in: date, check_out: date) -> BookingStatus:
    today = date.today()

    if check_in > check_out:
        raise ValueError("Дата выезда не может быть раньше даты заезда")

    if today >= check_in and today <= check_out:
        return BookingStatus.SETTLED
    elif today < check_in:
        return BookingStatus.WAITING
    else:
        return BookingStatus.EVICTED




class Booking:
    def __init__(self, customer, room, check_in_date, check_out_date,
                 status: BookingStatus, breakfast=False, product_intolerance=None):
        if check_in_date >= check_out_date:
            raise ValueError("Дата выезда должна быть позже даты заезда")

        if not isinstance(status, BookingStatus):
            raise TypeError("Некорректный статус бронирования")

        self.customer = customer
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = status
        self.breakfast = breakfast
        self.product_intolerance = product_intolerance or []
