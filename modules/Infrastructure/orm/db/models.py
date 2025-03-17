from django.db import models
from modules.Entities.Room import Room

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


class Room(models.Model):
    categories = Room.CATEGORIES

class Booking(models.Model):
    #name = Customer.name
    #surname = Customer.surname
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room = models.CharField(max_length=10, choices=Room.categories)