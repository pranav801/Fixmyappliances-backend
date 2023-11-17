from rest_framework import serializers
from accounts.models import User
from .models import *
from booking.models import Booking
from accounts.serializers import UserList
from service.serializers import ServiceListSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone', 'role', 'profile_image', 'is_active']


class RevenueSerializer(serializers.ModelSerializer):
    user = UserList()
    booked_service = ServiceListSerializer()
    class Meta:
        model = Booking
        fields = ['booking_id','user','booked_service','booking_amount','date_of_booking','is_paid']