
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from accounts.token import create_jwt_pair_tokens
from accounts.models import User
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter

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


