from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# class User(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)
#     # password = models.CharField(max_length=200)
#     vehicle = models.CharField(max_length=20, default='Sedan');
#
#     def __str__(self):
#         return self.email


class RideDetail(models.Model):
    owner = models.CharField(max_length=200)
    owner_email = models.CharField(max_length=200,default="mosiqi1996@hotmail.com")
    driver = models.CharField(max_length=200, blank=True, null=True)
    sharable = models.BooleanField(default=False,blank=True,null=True)
    remaining_seats = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Open')

    destination = models.CharField(max_length=200, blank=True, null=True)
    arrival_time = models.DateTimeField(default=timezone.now)
    vehicle = models.CharField(max_length=20, default='Sedan')
    special_request = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.owner

class Ride(models.Model):
    user_role = models.CharField(max_length=20)
    party_size = models.IntegerField(default= 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,db_column='user')
    ride_detail = models.ForeignKey(RideDetail, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.owner