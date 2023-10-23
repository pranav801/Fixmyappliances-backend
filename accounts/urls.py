from django.urls import path, include
from . import views
from . views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.get_routes),
    path('register/', UserRegistration.as_view()),
    path('activate/<uidb64>/<token> ', views.activate, name='activate'),

    path('forgot-password/', ForgotPassword.as_view()),
    path('reset-validate/<uidb64>/<token> ',
         views.reset_validate, name='reset_validate'),
    path('reset-password/', ResetPassword.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google_authentication/', GoogleAuthentication.as_view()),
    path('update/<int:id>',UpdateUser.as_view()),

    path('address/', AddressFill.as_view()),
    path('address/select/<int:user_id>', AddressSeclect.as_view()),

    path('userlist/<int:id>/', UserList.as_view()),

]


