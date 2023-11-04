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
    path('is-user-auth/<int:id>/', views.IsUserAuth.as_view(), name='user-auth'),

    path('address/', AddressFill.as_view()),
    path('address/select/<int:user_id>', AddressSeclect.as_view()),

    # path('userlist/<int:id>/', UserList.as_view()),
    path("user-previous-chats/<int:booking_id>/", PreviousMessagesView.as_view()),
    path("user-chat-list/<int:user_id>/", UserChatListView.as_view()),
    path("employee-chat-list/<int:employee_id>/", EmployeeChatListView.as_view()),
    path("set-chat-flag/<int:booking_id>/", SetChatFlag.as_view()),
    

    path('user-profile-detail/<int:id>/', UserDetailView.as_view()),
    path('users-profile-update/<int:user_id>', UserUpdateView.as_view()),
    path('update-profile-image/<int:id>', UserProfileImageView.as_view()),
    path('remove-profile-image/<int:id>', views.RemoveProfileImageView.as_view()),

]


