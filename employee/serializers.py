from rest_framework import serializers
from accounts.models import User

class EmployeeRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']

    