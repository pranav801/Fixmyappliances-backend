from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User,Address
from .serializers import *
from .token import create_jwt_pair_tokens
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from message.serializer import MessageSerializer
from message.models import Message
from booking.models import Booking
from rest_framework.generics import RetrieveUpdateAPIView


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/token/',
        '/token/refresh',
    ]
    return Response(routes)

class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password =request.data.get('password')

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('user/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite' : current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'A verificaiton link sent to your registered email address', "data": serializer.data})
        else:
            return Response({'status': 'error', 'msg': serializer.errors})


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
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message
        
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GoogleAuthentication(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if not User.objects.filter(email=email).exists():
            serializer = GoogleAuthSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.is_active = True
                user.set_password(password)
                user.save()

        user = authenticate(request, email=email, password=password)
        if user is not None:

            tokens = create_jwt_pair_tokens(user)
            response = {
                'msg': "Login successfull",
                'token': tokens,
                'status': 200
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={'msg': 'Login Failed', 'status': 400})


class ForgotPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('user/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'Please reset password by verifying the link', 'user_id': user.id})
        else:
            return Response({'status': 'error', 'msg': 'No account registered with this email'})


@api_view(['GET'])
def reset_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
       
        return HttpResponseRedirect(f'http://localhost:5173/reset-password/')


class ResetPassword(APIView):
    def post(self, request, format=None):
        str_user_id = request.data.get('user_id')
        uid = int(str_user_id)
        password = request.data.get('password')

        if uid:
            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()

            return Response({'msg': 'Password reset succesfully'})

        return HttpResponseRedirect('http://localhost:5173/login/')
    


class IsUserAuth(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id, is_active=True)
            return Response(data={'success': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'failure': False}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUser(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserRegisterSerializer


class AddressFill(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressSeclect(ListAPIView):
    def get(self, request, user_id):
        try:
            addresses = Address.objects.filter(user_id=user_id)
            serializer = AddressSerializer(addresses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response("User address not found", status=status.HTTP_404_NOT_FOUND)
    

class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserList
    lookup_field = 'id'


class UserUpdateView(APIView):
    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data  
        fields_to_update = {}

        for field in data:
            if field in ['first_name', 'last_name', 'phone']:
                fields_to_update[field] = data[field]

        serializer = UserUpdateSerializer(user, data=fields_to_update, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileImageView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileImageUpdateSerializer
    lookup_field = 'id'


class RemoveProfileImageView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileImageUpdateSerializer
    lookup_field='id'


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        booking_id = self.kwargs['booking_id']
        thread_name = 'chat_'+str(booking_id)
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset


class UserChatListView(APIView):
    def get(self,request,user_id):
        bookings = Booking.objects.filter(user__id=user_id).exclude(status='pending')
        result = []
        for booking in bookings:
            result.append({'user':booking.user.first_name,
                           'employee':booking.employee.employee.first_name,
                           'id':booking.id,
                           'service':booking.booked_service.service_name,
                           'chat_flag':booking.chat_flag,
                           })
        return Response(data= result)

class EmployeeChatListView(APIView):
    def get(self,request,employee_id):
        bookings = Booking.objects.filter(employee__id=employee_id).exclude(status='pending')
        result = []
        for booking in bookings:
            result.append({'employee':booking.employee.employee.first_name,
                           'user_id':booking.user.id,
                           'user':booking.user.first_name,
                           'id':booking.id,
                           'service':booking.booked_service.service_name,
                           'chat_flag':booking.chat_flag,
                           })
        return Response(data= result)

class SetChatFlag(APIView):
    def get(self,request,booking_id):
        try:
            return Response(data=Booking.objects.get(id=booking_id).chat_flag)
        except:
            return Response(status=400)
        