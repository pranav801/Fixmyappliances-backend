from django.urls import path, include
from . import views
from . views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    
    
]