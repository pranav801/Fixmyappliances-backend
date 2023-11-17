from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.AdminLogin.as_view()),
    path('is-admin-auth/<int:id>/', views.IsAdminAuth.as_view()),
    path('list-users/', views.ListUsers.as_view()),
    path('manage-user/<int:pk>/', views.ManageUser.as_view()),
    path('adminsearchUser/', views.AdminSearchUser.as_view()),
    # path('employeeRequest/',views.EmployeeRequestList.as_view()),
    # path('adminsearchEmployeeReq/',views.AdminSearchEmployeeReq.as_view()),
    path('employeeRequest/', views.EmployeeRequestList.as_view()),
    path('employeeRequest/<int:pk>/accept/', views.EmployeeRequestList.as_view(), {'action': 'accept'}, name='employee-accept'),
    path('employeeRequest/<int:pk>/reject/', views.EmployeeRequestList.as_view(), {'action': 'reject'}, name='employee-reject'),

    path('dashboard/', views.DashboardView.as_view()),
    path('revenue-list/', views.RevenueListView.as_view()),
]
