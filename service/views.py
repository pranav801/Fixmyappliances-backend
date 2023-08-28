from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView

from .serializers import *


class CategoryListView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryCreateAPIView(CreateAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


class CategoryDeleteApiView(DestroyAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    lookup_field='id'


class CategoryEditApiView(UpdateAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    lookup_field='id'

class ProductListView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()

class ProductDeleteApiView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field='id'


class ProductEditApiView(UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field='id'

class ServiceListView(ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceCreateAPIView(CreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

class ServiceDeleteApiView(DestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    lookup_field='id'


class ServiceEditApiView(UpdateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    lookup_field='id'
