from django.urls import path
from . views import *

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate_emp'),
    path('update-profile/<int:id>/', UpdateProfile.as_view()),
    path('complete-profile/<int:employee__id>/',ProfileCompletionView.as_view()),
    path('employeeDetailView/<int:employee__id>/',EmployeeDetailView.as_view()),
    path('login/', EmployeeSignIn.as_view()),
]
