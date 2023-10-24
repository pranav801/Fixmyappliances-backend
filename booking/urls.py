from django.urls import path
from .views import *

urlpatterns = [
    path('employees/available/<int:user_id>/', EmployeeListing, name='employee-list-api'),
    path('employees/create/', BookingCreateView.as_view(), name='booking-create'),
    path('payment-success/<str:bookingId>/', PaymentSuccess.as_view()),
    path('bookings-list/<int:userid>/', BookingsList.as_view()),
    # path('payment/stripe/', StripeCheckoutView.as_view(), ),
    path('last-pending-booking/<int:user_id>/', LastPendingBookingView.as_view(), name='last-pending-booking'),
    path('user-with-employee-by-booking/<int:BookingId>/', UserWithEmployeeByBookingId.as_view(), name='user-with-employee-by-booking'),
    path('booking-list-employee/<int:empid>/', BookingListEmployee.as_view()),
    path('update-booking-status/<int:booking_id>/', BookingStatusUpdate.as_view(), name='update-booking-status'),
    path('update-service-date-time/<int:booking_id>/', UpdateServiceDateAndTime.as_view()),
    path('admin-booking-list/', AdminBookingList.as_view()),
]


