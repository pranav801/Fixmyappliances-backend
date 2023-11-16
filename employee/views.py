from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from accounts.serializers import UserUpdateSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect
from .serializers import *
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from .models import Employee
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.token import *
from django.urls import reverse
from booking.models import Booking
from django.db.models import Sum
from django.contrib.auth import authenticate
from django.conf import settings
class EmployeeRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')

        serializer = EmployeeRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.role = 'employee'
            user.is_staff = True
            user.save()
            Employee.objects.create(employee=user)

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('employee/employee_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite': current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'A verificaiton link sent to your registered email address', "data": serializer.data})
        else:
            return Response({'status': 'error', 'msg': serializer.errors}, status=400)


@api_view(['GET'])
def empactivate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Congrats! Account activated!'
        redirect_url = f'{settings.SITE_URL}employee/form/' + \
            '?emp=' + str(user.id) + '&&message=' + message

    
    else:
        message = 'Invalid activation link'
        redirect_url = f'{settings.SITE_URL}employee/form/' + \
            '?emp=' + str(user.id)+'&&message=' + message


    return HttpResponseRedirect(redirect_url)


class UpdateProfile(UpdateAPIView):
    lookup_field = 'id'
    queryset = User.objects.filter(role='employee')
    serializer_class = BaseProfileSerializer


class ProfileCompletionView(UpdateAPIView):
    lookup_field = 'employee__id'
    queryset = Employee.objects.all()
    serializer_class = ProfileCompletionSerializer


class EmployeeDetailView(ListAPIView):
    lookup_field = 'employee__id'
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@api_view(['GET'])
def employee_detail(request, id):
    try:
        emp = Employee.objects.get(employee__id=id)
    except Employee.DoesNotExist:
        return Response("Employee not found", status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(emp)
    return Response(serializer.data)


class EmployeeSignIn(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user and user.role == 'employee':
            login(request, user)
            employee = Employee.objects.get(employee=user)
            # Generate a JWT token for the user
            data = create_jwt_pair_tokens(user, employee)
            return Response(data)
        else:
            return Response({'detail': 'Invalid credentials or insufficient permissions'}, status=status.HTTP_401_UNAUTHORIZED)



class EmployeePasswordChange(APIView):
    def post(self,request):
        userid = request.data.get('userid')
        old_password = request.data.get('current_password')

        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if user and user.check_password(old_password):
            return Response(data={'message': 'Password reset succesfully'}, status=status.HTTP_200_OK)
       
        else:
            return Response({'msg':'enter valid password'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def patch(self, request, format=None):
        userid = request.data.get('userid')
        password = request.data.get('password')

        if userid:
            user = User.objects.get(id=userid)
            user.set_password(password)
            user.save()
            emp = Employee.objects.get(employee=userid)
            print(emp)
            emp.isChangePassword = True
            emp.save()
            return Response({'msg': 'Password reset succesfully'},status=status.HTTP_202_ACCEPTED)


class PasswordChangeCheck(APIView):
    def get(self,request,userid):
        try:
            emp = Employee.objects.get(id=userid)
        except Employee.DoesNotExist:
            return Response("Employee not found", status=status.HTTP_404_NOT_FOUND)

        serializer = passwordChangeCheckSerializer(emp)

        return Response(serializer.data)
        
        

class EmployeeUpdateProfile(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'



@api_view(['PATCH'])
def EmployeeUpdate(request, employee__id):
    try:
        emp = Employee.objects.get(employee__id=employee__id)
    except Employee.DoesNotExist:
        return Response("Employee not found", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = EmployeSerializer(emp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDashboardView(APIView):
    def get(self, request, employee_id, format=None):
        pending_booking = Booking.objects.filter(
            employee__id=employee_id, status='pending').count()
        completed_work = Booking.objects.filter(
            employee__id=employee_id, status='completed').count()
        confirmed_works = Booking.objects.filter(
            employee__id=employee_id, status='confirmed').count()
        total_work_charge = Booking.objects.filter(employee__id=employee_id, status='completed').aggregate(
            total_booking_amount=Sum('booking_amount'))['total_booking_amount']
        if not total_work_charge:
            total_work_charge = 0
        commission = 0
        if total_work_charge > 10000:
            amount = total_work_charge - 10000
            commission = amount * 0.05

        data = {
            'pending_booking': pending_booking,
            'completed_work': completed_work,
            'confirmed_works': confirmed_works,
            'total_work_charge' : total_work_charge,
            'commission': commission,
        }

        return Response(data)
