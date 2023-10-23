from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect
from .serializers import EmployeeRegisterSerializer, ProfileCompletionSerializer, BaseProfileSerializer, EmployeeSerializer,EmployeeLoginSerializer
from rest_framework.generics import CreateAPIView,UpdateAPIView, ListAPIView
from .models import Employee
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.token import *

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
            message = render_to_string('user/account_verification.html', {
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
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Congrats! Account activated!'
        redirect_url = 'http://localhost:5173/employee/form/' + \
            '?emp=' + str(user.id)
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/employee/form/' + \
            '?emp=' + str(user.id)

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


class EmployeeSignIn(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
      
        if user and user.role == 'employee':
            login(request, user)
            employee = Employee.objects.get(employee=user)
            # Generate a JWT token for the user
            data = create_jwt_pair_tokens(user,employee)
            return Response(data)
        else:
            return Response({'detail': 'Invalid credentials or insufficient permissions'}, status=status.HTTP_401_UNAUTHORIZED)
        

        