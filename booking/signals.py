from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaints
from django.dispatch import Signal
from .utils import send_complaint_status_email

complaint_update_signal = Signal()

def send_employee_request_signal(complaint):
    complaint_update_signal.send(sender=complaint.__class__, complaint=complaint)

@receiver(post_save, sender=Complaints)
def send_status_update_email(sender, instance, created, **kwargs):
    if not created:

        send_complaint_status_email(
            instance.user.email,
            instance.user.first_name,
            instance.booking_id,
            instance.status,
        )
      
