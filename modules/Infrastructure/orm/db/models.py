from django.db import models


class Customer(models.Model):
    GENDERS = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    ]

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField()
    passport_id = models.JSONField()
    gender = models.CharField(max_length=10, choices=GENDERS)


class Room(models.Model):
    CATEGORIES = [
        ('BASE', 'Base'),
        ('LUX', 'Lux'),
        ('PREMIUM', 'Premium')
    ]

    number = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORIES)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('settled', 'Settled'),
        ('extended', 'Extended'),
        ('evicted', 'Evicted')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    breakfast = models.BooleanField(default=False)
    product_intolerance = models.JSONField(null=True, blank=True)