from django.db import models
from accounts.models import User,Address
from employee.models import Employee
from service.models import Products, Service
# Create your models here.


class Booking(models.Model):
    booking_id = models.UUIDField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    booked_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    booked_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_amount = models.PositiveIntegerField()
    date_of_booking = models.DateField(auto_now_add=True)
    time_of_booking = models.TimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    
