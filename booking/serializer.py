from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','address', 'employee', 'booked_product', 'booked_service', 'booking_amount','booking_id']

        