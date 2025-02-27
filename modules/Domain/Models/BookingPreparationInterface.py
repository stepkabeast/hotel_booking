from abc import ABC, abstractmethod
from typing import Dict, Any

class BookingPreparation(ABC):

    """
    Интерфейс предварительной обработки данных
    """

    @abstractmethod
    def get_customer_info(self, name: str, surname: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def check_room_availability(self, room_id: int, check_in_date, check_out_date) -> bool:
        raise NotImplementedError
