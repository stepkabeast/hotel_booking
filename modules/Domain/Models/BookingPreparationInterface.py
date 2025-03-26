from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BookingPreparation(ABC):
    """Интерфейс для получения информации о клиенте."""

    @abstractmethod
    def get_customer_info(self, name: str, surname: str) -> Dict[str, Any]:
        """Возвращает информацию о клиенте в виде словаря."""
        raise NotImplementedError

    @abstractmethod
    def check_rooms(self) -> List[int]:
        """Возвращает информацию о статусе номеров"""
        pass