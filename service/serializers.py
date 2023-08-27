from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Products
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Service
        fields = '__all__'