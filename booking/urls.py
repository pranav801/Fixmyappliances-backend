from django.urls import path
from .views import *

urlpatterns = [
    path('employees/available/<int:user_id>/', EmployeeListing, name='employee-list-api'),
    path('employees/create/', BookingCreateView.as_view(), name='booking-create'),
    path('payment-success/<str:bookingId>/', PaymentSuccess.as_view()),
    # path('payment/stripe/', StripeCheckoutView.as_view(), ),
]


