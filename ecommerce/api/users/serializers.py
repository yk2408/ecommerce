from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import request
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from userprofile.models import UserProfile
from userprofile.tokens import account_activation_token, password_reset_token
from userprofile.views import send_mail

GENDER_CHOICES = [
                    ('M', 'Male'),
                    ('F', 'Female')
                 ]


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(error_messages={
        'required': "First name is required",
        'invalid': "Please enter valid first name",
        'blank': "First name should not be blank",
    })
    last_name = serializers.CharField(error_messages={
        'required': "Last name is required",
        'invalid': "Please enter valid last name",
        'blank': "Last name should not be blank",
    })
    username = serializers.CharField(error_messages={
        'required': "Username is required",
        'invalid': "Please enter valid username",
        'blank': "Username should not be blank",
    })
    email = serializers.EmailField(error_messages={
        'required': "Email is required",
        'invalid': "Please enter valid email",
    })
    password = serializers.CharField(
        max_length=20,
        min_length=8,
        write_only=True,
        error_messages={
            'required': "Password is required",
            'invalid': "Please enter valid password",
            'min_length': "Password should contain minimum 8 characters",
            'max_length': "Password should not contain more then 20 characters",
            'blank': "Password should not be blank"
        }
    )
    confirm_password = serializers.CharField(
        max_length=20,
        min_length=8,
        write_only=True,
        error_messages={
            'required': "Confirm Password is required",
            'invalid': "Please enter valid Confirm password",
            'blank': "Confirm Password should not be blank"
        }
    )
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
        error_messages={
            'required': "Gender is required",
            'invalid': "Please enter choose valid Gender",
            'blank': "Gender should not be blank"
        }
    )
    mobile_number = serializers.CharField(
        max_length=10,
        error_messages={
            'required': "Mobile Number is required",
            'invalid': "Please enter valid Mobile Number",
            'max_length': "Mobile Number should contain 10 digits",
            'blank': "Mobile Number should not be blank"
        }
    )
    profile_pic = serializers.ImageField(
        use_url='profile',
        required=False
    )

    def validate(self, data):
        # Username Validation
        username = User.objects.filter(username=data['username']).count()
        if username >= 1:
            raise serializers.ValidationError('User with this username already Exists')

        # Email Validation
        email = User.objects.filter(email=data['email']).count()
        if email >= 1:
            raise serializers.ValidationError('User with this email already Exists')

        # Confirm Password Matched Validation
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Confirm Password not matched')
        return data

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        password = validated_data.get('password')
        gender = validated_data.get('gender')
        mobile_number = validated_data.get('mobile_number')
        profile_pic = validated_data.get('profile_pic')
        email = validated_data.get('email')
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, gender=gender, mobile_number=mobile_number, profile_pic=profile_pic)
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={
        'required': "Username is required",
        'invalid': "Please enter valid username",
        'blank': "Username should not be blank",
    })
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': "Password is required",
            'invalid': "Please enter valid password",
            'blank': "Password should not be blank"
        }
    )
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'username': user.username,
            'token': jwt_token
        }


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'required': "Email is required",
        'invalid': "Please enter valid email",
    })

    def validate(self, data):
        current_site = Site.objects.get_current()
        mail_subject = 'Reset Password of your account'
        to_email = data.get('email')
        try:
            user = User.objects.get(email=to_email)
            if user:
                message = render_to_string('reset-password-api-email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user)
                                       })
                mail_send = send_mail(mail_subject, to_email, message)

                if mail_send == "un-success":
                    raise serializers.ValidationError('The email account is does not exist. please enter the email address associated with your account')

        except User.DoesNotExist:
            raise serializers.ValidationError('The email account is does not exist. please enter the email address associated with your account')

        return data


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=20,
        min_length=8,
        write_only=True,
        error_messages={
            'required': "Password is required",
            'invalid': "Please enter valid password",
            'min_length': "Password should contain minimum 8 characters",
            'max_length': "Password should not contain more then 20 characters",
            'blank': "Password should not be blank"
        }
    )
    confirm_password = serializers.CharField(
        max_length=20,
        min_length=8,
        write_only=True,
        error_messages={
            'required': "Confirm Password is required",
            'invalid': "Please enter valid Confirm password",
            'blank': "Confirm Password should not be blank"
        }
    )

    def validate(self, data):
        uidb64 = self.context.get("uidb64")
        token = self.context.get("token")
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(ValueError, TypeError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and password_reset_token.check_token(user, token):
            password = data.get('new_password')
            user.set_password(password)
            user.save()
        else:
            raise serializers.ValidationError('Password Reset link is invalid')
        return data


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(error_messages={
        'required': "First name is required",
        'invalid': "Please enter valid first name",
        'blank': "First name should not be blank",
    })
    last_name = serializers.CharField(error_messages={
        'required': "Last name is required",
        'invalid': "Please enter valid last name",
        'blank': "Last name should not be blank",
    })
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(error_messages={
        'required': "Email is required",
        'invalid': "Please enter valid email",
    })
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
        error_messages={
            'required': "Gender is required",
            'invalid': "Please enter choose valid Gender",
            'blank': "Gender should not be blank"
        }
    )
    mobile_number = serializers.CharField(
        max_length=10,
        error_messages={
            'required': "Mobile Number is required",
            'invalid': "Please enter valid Mobile Number",
            'max_length': "Mobile Number should contain 10 digits",
            'blank': "Mobile Number should not be blank"
        }
    )
    profile_pic = serializers.ImageField(
        use_url='profile',
        required=False
    )

    def to_representation(self, instance):
        data = {
                'username': instance.user.username,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'email': instance.user.email,
                'gender': instance.gender,
                'mobile_number': instance.mobile_number,
                }

        try:
            data.update({'profile_pic', instance.profile_pic})
        except ValueError:
            profile_pic = None

        return data

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.save()
        return instance
