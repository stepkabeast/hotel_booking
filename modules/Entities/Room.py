from typing import Tuple


class Room:
    CATEGORIES = [('BASE', 'Base'), ('LUX', 'Lux'), ('PREMIUM', 'Premium')]

    category: str
    number: Tuple
    def __init__(self, category: str, number: Tuple):
        self.category = category
        self.number = number
        
