from rest_framework import serializers
from .models import Booking,ReviewRating,Complaints
from employee.serializers import EmployeeSerializer
from accounts.serializers import UserList,AddressSerializer
from service.serializers import ProductSerializer,ServiceSerializer

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','address', 'employee', 'booked_product', 'booked_service', 'booking_amount','booking_id']

class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingsSerializer(serializers.ModelSerializer):
    user = UserList()
    employee = EmployeeSerializer()
    address = AddressSerializer()
    booked_product = ProductSerializer()
    booked_service = ServiceSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'

class ReviewListingSerializer(serializers.ModelSerializer):
    user = UserList()
    product = ProductSerializer()
    class Meta:
        model = ReviewRating
        fields = '__all__'



class ComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = '__all__'

class ComplaintListSerializer(serializers.ModelSerializer):
    user = UserList()
    class Meta:
        model = Complaints
        fields = '__all__'
        