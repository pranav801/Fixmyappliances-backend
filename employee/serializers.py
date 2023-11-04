from rest_framework import serializers
from accounts.models import User
from employee.models import Employee
from service.serializers import CategorySerializer,ProductSerializer
from superuser.serializers import UserSerializer
class EmployeeRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']

class BaseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

class ProfileCompletionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Employee
        fields = '__all__'
    def update(self, instance, validated_data):
        # Update the fields from the request data
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.category = validated_data.get('category', instance.category)
        instance.product.set(validated_data.get('product', instance.product.all()))

        # Set isRequested to True
        instance.isRequested = True

        # Save the instance
        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    category = CategorySerializer()
    product = ProductSerializer(many = True)
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    class Meta:
        model = Employee
        fields = ['employee']




class EmployeeLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

