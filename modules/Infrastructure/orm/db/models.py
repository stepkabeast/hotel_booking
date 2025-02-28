from django.db import models


class Customer(models.Model):
    GENDERS = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]

    gender = models.CharField(max_length=10, choices=GENDERS)
    age = models.IntegerField()
    passport_id = models.JSONField() # Используем JSONField для словаря
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}"