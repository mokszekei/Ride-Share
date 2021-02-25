from django.db import models
from django.contrib.auth.models import User

class Rider(User):
    phone = models.BigIntegerField()
    cardInfo = models.BigIntegerField()

    def __str__(self):
        return f'Rider {self.user.username}'

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField()
    licenseNum = models.CharField(max_length=100)
    Vtype = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plateNum = models.CharField(max_length=100)
    max_pnum = models.IntegerField()
    special_info = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Driver {self.user.username}'