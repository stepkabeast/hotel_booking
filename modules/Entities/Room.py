from typing import Dict, Any


class Room:
    CATEGORIES = [('BASE', 'Base'), ('LUX', 'Lux'), ('PREMIUM', 'Premium')]

    def __init__(self, category: str, number: str):  # Изменено на str
        self.category = category
        self.number = number

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        return cls(
            category=data['category'],
            number=data['number']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'number': self.number,
            'status': 'available'
        }