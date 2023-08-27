from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.AdminLogin.as_view()),
    path('list-users/', views.ListUsers.as_view()),
    path('manage-user/<int:pk>/', views.ManageUser.as_view()),
    path('adminsearchUser/', views.AdminSearchUser.as_view()),
]
