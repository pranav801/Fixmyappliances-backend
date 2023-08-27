from django.urls import path
from . import views
from . views import *

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view()),
    path('activate/<uidb64>/<token> ', views.activate, name='activate'),    
]