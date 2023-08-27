from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializers import *


class CategoryListView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


