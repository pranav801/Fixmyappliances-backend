from django.db import models
from accounts.models import User
from employee.models import Employee
from booking.models import Booking


class Message(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,null=True,on_delete=models.CASCADE)
    sender = models.CharField(null=True,max_length=200)
    message = models.TextField(null=True)
    thread_name = models.CharField(null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'({self.thread_name})'
    
