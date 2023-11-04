from django.urls import path, include
from . import views
from . views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('categories/create/', CategoryCreateAPIView.as_view()),
    path('categories/delete/<int:id>/', CategoryDeleteApiView.as_view()),
    path('categories/edit/<int:id>/',CategoryEditApiView.as_view()),
    
    path('product/', ProductListView.as_view()),
    path('product/create/', ProductCreateAPIView.as_view()),
    path('product/delete/<int:id>/', ProductDeleteApiView.as_view()),
    path('product/edit/<int:id>/',ProductEditApiView.as_view()),
    
    path('services/', ServiceListView.as_view()),
    path('services/create/', ServiceCreateAPIView.as_view()),
    path('services/delete/<int:id>/', ServiceDeleteApiView.as_view()),
    path('services/edit/<int:id>/',ServiceEditApiView.as_view()),

    path('services/list/', ServiceViewSet.as_view()),

    path('product/listing/<int:category_id>/',ProductListing.as_view()),

    path('product/products/<str:categoryName>/' ,ProductsByCategory.as_view()),
    path('product/detail/<str:productName>/', ServiceByProduct.as_view()),
    path('search/', SearchView.as_view(), name='search'),
]


