from django.db import models
from accounts.models import User
from service.models import Category,Products

from django.db.models.signals import post_save
from django.dispatch import receiver
from superuser.utils import send_employee_status_email


class Employee(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(Products)
    pincode = models.IntegerField(null=True)
    isVerified = models.BooleanField(default=False)
    isRequested = models.BooleanField(default=False)
    isChangePassword = models.BooleanField(default=False)

from django.dispatch import Signal

# @receiver(post_save, sender=Employee)
employee_request_signal = Signal()

def send_employee_request_signal(employee, temp_password=None):
    employee_request_signal.send(sender=employee.__class__, employee=employee, temp_password=temp_password)

@receiver(employee_request_signal, sender=Employee)
def employy_request(sender, instance, created, temp_password, **kwargs):
    if not created:
        
        send_employee_status_email(
            instance.employee.email,
            instance.employee.first_name,
            instance.isVerified,
            temp_password,
        )
