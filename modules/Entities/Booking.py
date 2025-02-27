from modules.Entities.Customer import Customer
from modules.Entities.Room import Room
from enum import Enum

class BookingStatus(str, Enum):
    WAITING = 'waiting'
    SETTLED = 'settled'
    EXTENDED = 'extended'
    EVICTED = 'evicted'


class Booking:

    status: BookingStatus
    customer: Customer | None
    room: Room
    check_in_date: str
    check_out_date: str
    breakfast: bool | None = None
    product_intolerance: list | None = None


    def __init__(
            self,
            status: BookingStatus,
            customer: Customer | None,
            room: Room | None,
            check_in_date: str,
            check_out_date: str,
            breakfast: bool | None = None,
    ):
        if breakfast:
            self.product_intolerance = breakfast
        self.status = status
        self.customer = customer
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def check_room(self, number) -> bool:
        if (number == self.room.number) and (self.status == BookingStatus.WAITING):
            return True
        else:
            return False






