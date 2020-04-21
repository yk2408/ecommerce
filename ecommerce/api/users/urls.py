from django.urls import path, re_path
from .views import UserSignupApi, UserLoginApi, UserLogoutApi, UserForgotPasswordApi, UserResetPasswordApi, UserProfileDetailsApi


urlpatterns = [
    path('users/signup/', UserSignupApi.as_view(), name='signup-api'),
    path('users/login/', UserLoginApi.as_view(), name='login-api'),
    path('users/forgot-password/', UserForgotPasswordApi.as_view(), name='forgot-password-api'),
    path('users/logout/', UserLogoutApi.as_view(), name='logout-api'),
    re_path(
                r'users/reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                UserResetPasswordApi.as_view(), name='reset-password-api'
            ),
    path('userprofile/details/get/<int:pk>/', UserProfileDetailsApi.as_view(), name='profile-get-api'),
    path('userprofile/details/update/<int:pk>/', UserProfileDetailsApi.as_view(), name='profile-update-api')
]