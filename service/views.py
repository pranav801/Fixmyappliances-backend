from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status

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
    serializer_class = ProductListSerializer
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

class ServiceViewSet(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    
class ProductListing(APIView):
    def get(self, request, category_id):
        products = Products.objects.filter(product_cat__id=category_id)
        result = ProductListSerializer(products,many=True).data
        return Response(result)

class ProductsByCategory(APIView):

    def get(self, request, categoryName):
        try:
            product = Products.objects.filter(product_cat__category_name=categoryName)
            
            serializer = ProductListSerializer(product, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"Error fetching products by category. {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ServiceByProduct(APIView):

    def get(self, request, productName):
        try:
            product = Service.objects.filter(service_product__product_name=productName)
            
            serializer = ServiceListSerializer(product, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"Error fetching services by product. {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)