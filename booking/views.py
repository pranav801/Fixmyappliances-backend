from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView,CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from employee.models import Employee
from .serializer import BookingSerializer,BookingListSerializer,BookingsSerializer
from employee.serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from accounts.models import Address
from service.models import Service
import stripe
from django.conf import settings
import uuid


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def EmployeeListing(request, user_id):
    try:
        
        address = Address.objects.filter(user__id=user_id).last()

        employees = Employee.objects.filter(pincode=address.pincode)
        
        serialized_employees = EmployeeSerializer(employees, many=True)  
        return Response(serialized_employees.data, status=status.HTTP_200_OK)
    except Address.DoesNotExist:
        return Response("Address not found for the user", status=status.HTTP_404_NOT_FOUND)
    

    
class BookingCreateView(APIView):
    def post(self, request, format=None):
       
        user_id = request.data.get('user')
        employee_id = request.data.get('employee')
        service_id = request.data.get('service')

       
        user_address = Address.objects.filter(user__id=user_id).last()
        service = Service.objects.get(id=service_id)

        if user_address is None:
            return Response({'message': 'User address not found'}, status=status.HTTP_400_BAD_REQUEST)

        if service is None:
            return Response({'message': 'Service not found'}, status=status.HTTP_400_BAD_REQUEST)

        booking_amount = service.service_charge
        booking_id = uuid.uuid1()

        booking_data = {
            'user': user_id,
            'employee': employee_id,
            'booked_service': service_id,
            'address': user_address.id,
            'booked_product': service.service_product.id,
            'booking_amount': booking_amount,
            'booking_id': booking_id
        }

        serializer = BookingSerializer(data=booking_data)
        flag = False
        if serializer.is_valid():
            serializer.save()
            flag = True
        

        if flag == True:
            try:
                checkout_session = stripe.checkout.Session.create(
                    line_items=[{
                        'price_data': {
                            'currency': 'INR',
                            'product_data': {
                                'name': service.service_name,
                            },
                            'unit_amount': service.service_charge * 100
                        },
                        'quantity': 1
                    }],
                    payment_method_types = ['card',],
                    mode='payment',
                    success_url= settings.SITE_URL + 'service/payment/?booking=' + str(booking_id),
                    cancel_url= settings.SITE_URL + '?canceled=true',
                )

                return Response(data=checkout_session.url, status=status.HTTP_201_CREATED)
            except:
                return Response({'error':'something went wrong when creating stripe checkout'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error':'Address not saved'},status=status.HTTP_200_OK)
       
   
class PaymentSuccess(APIView):
    def patch(self,request,bookingId):
        try:
            booking = Booking.objects.get(booking_id = bookingId)
            booking.is_paid = True
            booking.save()
            return Response(data={'message' : 'Success'}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response(data={'message' : 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        

class BookingsList(ListAPIView):
    serializer_class = BookingsSerializer

    def get_queryset(self):
        userid = self.kwargs['userid']  
        return Booking.objects.filter(user=userid)
    

class LastPendingBookingView(RetrieveAPIView):
    serializer_class = BookingListSerializer

    def get(self, request, user_id):
        
        booking = Booking.objects.filter(user_id=user_id, status='pending').last()

        if booking is not None:
            serializer = self.serializer_class(booking)
            return Response(serializer.data)
        
        else:
            return Response({'message': 'No pending booking found for this user.'}, status=status.HTTP_404_NOT_FOUND)


        
class UserWithEmployeeByBookingId(APIView):
    def get(self, request, BookingId):
        try:
            booking = Booking.objects.get(id=BookingId)
            user = booking.employee.employee
            return Response(data={'name':user.first_name,'email':user.email})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        

class BookingListEmployee(ListAPIView):
    serializer_class = BookingsSerializer

    def get_queryset(self):
        empid = self.kwargs['empid']  
        return Booking.objects.filter(employee=empid) 


class BookingStatusUpdate(APIView):
    def patch(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status', None)

        if new_status is None or new_status not in dict(Booking.ROLE_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = new_status
        booking.save()

        serializer = BookingListSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UpdateServiceDateAndTime(APIView):
    def patch(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        service_date = request.data.get('service_date')
        service_time = request.data.get('service_time')

        if service_date is not None:
            booking.service_date = service_date

        if service_time is not None:
            booking.service_time = service_time

        booking.save()

        serializer = BookingListSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)