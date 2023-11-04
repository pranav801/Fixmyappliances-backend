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

class ProductListSerializer(serializers.ModelSerializer):
    product_cat = CategorySerializer()
    class Meta:
        model  = Products
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Service
        fields = '__all__'

class ServiceListSerializer(serializers.ModelSerializer):
    service_product = ProductSerializer()

    class Meta:
        model = Service
        fields = '__all__'

