from django.db import models
from accounts.models import User,Address
from employee.models import Employee
from service.models import Products, Service
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import send_complaint_status_email



class Booking(models.Model):
    ROLE_CHOICES = (
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),

    )

    booking_id      = models.UUIDField(null=True, unique=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    address         = models.ForeignKey(Address, on_delete=models.CASCADE)
    employee        = models.ForeignKey(Employee, on_delete=models.CASCADE)
    booked_product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    booked_service  = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_amount  = models.PositiveIntegerField()
    date_of_booking = models.DateField(auto_now_add=True)
    time_of_booking = models.TimeField(auto_now_add=True)
    service_date    = models.DateField(null=True)
    service_time    = models.TimeField(null=True)
    is_paid         = models.BooleanField(default=False)
    chat_flag       = models.BooleanField(default=False)
    status          = models.CharField(max_length=50, default='pending', choices=ROLE_CHOICES)


class ReviewRating(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    content = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)


class Complaints(models.Model):

    ROLE_CHOICES = (
        ('pending', 'pending'),
        ('resolved', 'resolved'),
        ('solved', 'solved'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.UUIDField()
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending', choices=ROLE_CHOICES)

@receiver(pre_save, sender=Complaints)
def send_email_on_status_update(sender, instance, **kwargs):
    if instance.pk:
        old_complaint = Complaints.objects.get(pk=instance.pk)
        if old_complaint.status != instance.status:
            subject = "Complaint Status Update"
            message = f"Your complaint with subject '{instance.subject}' has been updated to '{instance.status}'."
            send_complaint_status_email(instance.user.email, instance.user.first_name,instance.status,instance.booking_id)
