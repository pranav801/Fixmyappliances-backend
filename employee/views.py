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
from .serializers import EmployeeRegisterSerializer

class EmployeeRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')

        serializer = EmployeeRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
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
        redirect_url = 'http://localhost:5173/employee/home/' + '?message=' + message
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/employee/home/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)

