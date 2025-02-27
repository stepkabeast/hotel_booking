from typing import Tuple


class Room:
    BASE = 'Base'
    LUX = 'Luxury'
    PREMIUM = 'Premium'
    
    CATEGORIES = [BASE, LUX, PREMIUM]

    category: str
    number: Tuple
    def __init__(self, category: str, number: Tuple):
        self.category = category
        self.number = number
        
