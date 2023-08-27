import re
from rest_framework import serializers
from . models import User
from rest_framework.validators import ValidationError
from django.forms.models import model_to_dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        def validate(self, attrs):
            email_exist = User.objects.filter(email=attrs['email']).exists()
            # Email validation
            if email_exist:
                return ValidationError('This email is already exist')
            return super().validate(attrs)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if not user.is_active:
            raise ValidationError('User is not active', code='inactive_user')

    

        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['is_active'] = user.is_active
        token['is_google'] = user.is_google

        return token


