from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserProfile, SubscribeUser
import re


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First name', 'class': 'info'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last name', 'class': 'info'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'info'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email', 'class': 'info'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'info'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'info'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        c_password = self.cleaned_data.get('confirm_password')
        user_name = User.objects.filter(username=username)
        e_mail = User.objects.filter(email=email)
        if len(password) < 6:
            raise forms.ValidationError('Password should be at least 6 character')
        elif password != c_password:
            raise forms.ValidationError('Confirm Password not matched')
        elif e_mail.exists():
            raise forms.ValidationError('This email already used in another account')
        elif user_name.exists():
            raise forms.ValidationError('Username already exists')

        return super(UserForm, self).clean()


class RegisterForm(forms.ModelForm):
    CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = forms.CharField(widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'info'}))
    mobile_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'class': 'info'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'info'}), required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user', )

    def clean(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        mobile_number = str(mobile_number)
        pattern = re.compile("[6-9][0-9]{9}")
        reg = pattern.findall(mobile_number)
        if not reg:
            raise forms.ValidationError('Incorrect Mobile Number')
        return super(RegisterForm, self).clean()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'info'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'info'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'remr'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            hasher = identify_hasher(user.password)
            encoded = user.password
            is_correct = hasher.verify(password, encoded)
        except User.DoesNotExist:
            user = None
        if user is None:
            raise forms.ValidationError('Incorrect Username.. New User? Please Register First')
        elif not user.is_active:
            raise forms.ValidationError('Email not confirmed')
        elif not is_correct:
            raise forms.ValidationError('Password not matched')

        return super(LoginForm, self).clean()


class UpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'info', 'readonly': 'readonly'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'info'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'info'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'info'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        user2 = User.objects.filter(email=email).values('email')
        user1 = User.objects.filter(username=username).values('email')
        for i in user1:
            e_mail1 = i['email']
        for i in user2:
            if i:
                e_mail2 = i['email']
                if e_mail1 != e_mail2:
                    raise forms.ValidationError('This email already used')
                else:
                    return super(UpdateForm, self).clean()
            else:
                return super(UpdateForm, self).clean()

        return super(UpdateForm, self).clean()


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'class': 'info'}))

    def clean(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is None:
            raise forms.ValidationError('Please enter the email address associated with your account')

        return super(ForgotPasswordForm, self).clean()


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'info'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confirm Password', 'class': 'info'}))

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        print(new_password)
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(new_password) < 6:
            raise forms.ValidationError('Password should be at least 6 character')
        elif new_password != confirm_password:
            raise forms.ValidationError('Confirm Password not matched')

        return super(ResetPasswordForm, self).clean()


class SubscribeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Your Email hear', 'id': 'id_email'}))

    class Meta:
        model = SubscribeUser
        fields = ('email', )