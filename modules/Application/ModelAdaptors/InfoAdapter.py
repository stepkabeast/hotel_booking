from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BookingRepository(ABC):
    """
    Абстрактный класс для выполнения CRUD-операций с базой данных.
    """

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> int:
        """
        Returns:
            Идентификатор созданной записи.
        """
        pass

    # @abstractmethod
    # def read(self, id: int) -> Optional[Dict[str, Any]]:
    #     """
    #     Получает запись из базы данных по идентификатору.
    #
    #     Args:
    #         id: Идентификатор записи.
    #
    #     Returns:
    #         Словарь, содержащий данные записи, или None, если запись не найдена.
    #     """
    #     pass
    #
    # @abstractmethod
    # def update(self, id: int, data: Dict[str, Any]) -> bool:
    #     """
    #     Обновляет запись в базе данных по идентификатору.
    #
    #     Args:
    #         id: Идентификатор записи.
    #         data: Словарь, содержащий данные для обновления записи.
    #
    #     Returns:
    #         True, если запись успешно обновлена, False в противном случае.
    #     """
    #     pass
    #
    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Удаляет запись из базы данных по идентификатору.

        Args:
            id: Идентификатор записи.

        Returns:
            True, если запись успешно удалена, False в противном случае.
        """
        pass

    @abstractmethod
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получает список записей из базы данных с возможностью фильтрации.

        Args:
            filters: Словарь, содержащий условия фильтрации.

        Returns:
            Список словарей, содержащих данные записей.
        """
        pass