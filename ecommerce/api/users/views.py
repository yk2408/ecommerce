from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.base.views import BaseView, get_response
from api.common.authentication import CustomAuthentication
from rest_framework import serializers
from api.users.models import Blacklist
from userprofile.models import UserProfile
from .serializers import SignupSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, UserProfileSerializer

# User Signup Api View :-


class UserSignupApi(BaseView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Signed Up successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

# User Login Api View :-


class UserLoginApi(BaseView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = get_response(message='Login successful', result={"token": serializer.data['token']})
        return Response(response, status=response["status_code"])

# ForgotPassword Api View:-


class UserForgotPasswordApi(BaseView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = get_response(message='Firstly check your Email for reset your password', result={})
        return Response(response, status=response["status_code"])

# ResetPassword Api View :-


class UserResetPasswordApi(BaseView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64,
                   "token": token
                   }
        serializer = ResetPasswordSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        response = get_response(message='Password reset Successfully', result={})
        return Response(response, status=response["status_code"])


# User Logout Api View :-


class UserLogoutApi(BaseView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def post(self, request):
        token = request.META['HTTP_AUTHORIZATION'][4:]
        black_list = Blacklist(token=token)
        black_list.save()
        response = get_response(message='Logout successful')
        return Response(response, status=response["status_code"])

# User Profile Details View :-


class UserProfileDetailsApi(BaseView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Get Details :-
    def get(self, request, pk):
        userprofile_instance = self.get_object(pk)
        userprofile_details = UserProfileSerializer(userprofile_instance)
        response = get_response(message='Details Fetched successful', result=userprofile_details.data)
        return Response(response, status=response["status_code"])

    # Update Details :-
    def put(self, request, pk):
        userprofile_instance = self.get_object(pk)
        serializer = UserProfileSerializer(userprofile_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Update Profile successfully', result=serializer.data)
        return Response(response, status=response["status_code"])