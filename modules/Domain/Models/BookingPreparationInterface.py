from abc import ABC, abstractmethod
from typing import Dict, Any

class BookingPreparation(ABC):

    """
    Интерфейс предварительной обработки данных
    """

    @abstractmethod
    def get_customer_info(self, name: str, surname: str) -> Dict[str, Any]:
        raise NotImplementedError
