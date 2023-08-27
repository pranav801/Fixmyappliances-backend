from rest_framework import serializers
from accounts.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone', 'role', 'profile_image', 'is_active']
