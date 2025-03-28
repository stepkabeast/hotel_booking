class Room:
    CATEGORIES = [('BASE', 'Base'), ('LUX', 'Lux'), ('PREMIUM', 'Premium')]

    def __init__(self, category: str, number: str):
        self.category = category
        self.number = number
