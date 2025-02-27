class Customer:
    GENDERS = ['MALE', 'FEMALE']
    gender: str
    age: int
    passport_id: dict[str, str]
    name: str
    surname: str

    def __init__(self, name: str, surname: str, age: int, passport_id: dict[str, str], gender: str ):
        self.name = name
        self.surname = surname
        self.age = age
        self.passport_id = passport_id
        self.gender = gender

    def is_valid(self) -> bool:
        return (
            self.gender in self.GENDERS and
            isinstance(self.age, int) and self.age > 0 and
            isinstance(self.passport_id, dict) and
            isinstance(self.name, str) and self.name and
            isinstance(self.surname, str) and self.surname
        )


