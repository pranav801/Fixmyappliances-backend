
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from accounts.token import create_jwt_pair_tokens
from accounts.models import User
from employee.models import Employee,employee_request_signal
from .serializers import UserSerializer, RevenueSerializer
from employee.serializers import EmployeeSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view,action
from .utils import send_employee_status_email
from .helpers import generate_random_password
from booking.models import ReviewRating,Complaints,Booking
from service.models import Products, Service
from django.db.models import Count, Q, Sum, Avg, ExpressionWrapper, FloatField
from django.db.models.functions import Round



class AdminLogin(APIView): 
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')


        user = authenticate(request, email=email, password=password)
        print(f'User is {user}')

        if user is not None:
            if user.is_active and user.is_admin and user.role == 'admin':
                tokens = create_jwt_pair_tokens(user)
                response = {
                    'message': 'Login succesfull',
                    'token': tokens
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Unauthorized access'}
                return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)
        else:

            response = {'message': 'Invalid login credentials'}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class IsAdminAuth(APIView):
    def get(self, request, id):
        try:
            superadmin = User.objects.get(
                id=id, is_active=True, role='admin')
            return Response(data={'success': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'failure': False}, status=status.HTTP_404_NOT_FOUND)


class ListUsers(ListAPIView):
    queryset = User.objects.filter(role='user').order_by('-id')
    serializer_class = UserSerializer


class ManageUser(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk, role='user')
            user.is_active = not user.is_active
            user.save()
            if user.is_active:
                message = 'User Unblocked'
            else:
                message = 'User blocked'
            return Response(data={'message': message}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'message': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)


class AdminSearchUser(ListCreateAPIView):
     serializer_class = UserSerializer
     filter_backends = [SearchFilter]
     queryset = User.objects.filter(is_admin=False, is_staff=False)
     search_fields = ['first_name', 'last_name', 'email','phone']  


class EmployeeRequestList(APIView):
    serializer_class = EmployeeSerializer

    def get(self, request):
        queryset = Employee.objects.filter(isRequested=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk, action):
        employee = Employee.objects.get(pk=pk)

        if action=='accept':
            employee.isVerified = True
            message = 'Accepted'
            password = generate_random_password()
            temp_password = password
            employee.employee.set_password(password)
            employee.employee.save()
        elif action=='reject':
            employee.isVerified = False
            message = 'Rejected'
            temp_password = 'False'
        employee.save()

        # send_employee_status_email(employee, message, action,temp_password)
        employee_request_signal.send(sender=Employee, instance=employee, created=False, temp_password=temp_password)
        
        return Response({'message': message}, status=status.HTTP_200_OK)



class AdminSearchEmployeeReq(ListCreateAPIView):
    serializer_class = EmployeeSerializer
    filter_backends = [SearchFilter]
    queryset = Employee.objects.all()
    search_fields = ['employee__first_name','employee__last_name','employee__email','employee__phone','category__category_name','pincode']



class DashboardView(APIView):
    def get(self, request, format=None):
        users_count = User.objects.filter(role='user').count()
        employee_count = Employee.objects.filter(isVerified=True).count()
        employee_request_count = Employee.objects.filter(isRequested=True).count()
        complaints_pending = Complaints.objects.filter(status='pending').count()
        rating = rating = ReviewRating.objects.aggregate(avg_rating=ExpressionWrapper(Round(Avg('rating'), 2), output_field=FloatField()))

        products_count = Products.objects.all().count()
        service_count = Service.objects.all().count()
        booking_count = Booking.objects.aggregate(
                        pending_count=Count('id', filter=Q(status='pending')),
                        confirmed_count=Count('id', filter=Q(status='confirmed'))
                        )
        completed_work = Booking.objects.filter(status='completed').count()
        total_income = Booking.objects.aggregate(total_booking_amount=Sum('booking_amount'))
        
        data = {
            'users': users_count,
            'employee_count': employee_count,
            'employee_request_count': employee_request_count,
            'complaints_pending': complaints_pending,
            'rating': rating,

            'products_count': products_count,
            'service_count' : service_count,
            'booking_count' : booking_count['pending_count']+booking_count['confirmed_count'],
            'completed_work' : completed_work,
            'total_income' : total_income,
        }

        return Response(data)
    

class RevenueListView(ListAPIView):
    serializer_class = RevenueSerializer
    def get_queryset(self):
        month = self.request.query_params.get('month', None)

        queryset = Booking.objects.filter(is_paid=True)

        if month:
            queryset = queryset.filter(date_of_booking__month=month)

        return queryset