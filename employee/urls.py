from django.urls import path
from . views import *

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view()),
    path('activate/<uidb64>/<token>', empactivate, name='empactivate'),
    path('update-profile/<int:id>/', UpdateProfile.as_view()),
    path('complete-profile/<int:employee__id>/',ProfileCompletionView.as_view()),
    path('employeeDetailView/<int:employee__id>/',EmployeeDetailView.as_view()),
    path('employeeDetail/<int:id>/',employee_detail),
    path('login/', EmployeeSignIn.as_view()),
    path('profile-update/<int:id>/', EmployeeUpdateProfile.as_view()),
    path('profile-edit/<int:employee__id>', EmployeeUpdate),

    path('employee-dashboard/<int:employee_id>/', EmployeeDashboardView.as_view()),
]
