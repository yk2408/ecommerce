from django.conf import Settings, settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views.generic import UpdateView
from order.forms import ManageAddressForm, AddAddressForm
from order.models import ManageAddress
from .models import UserProfile, SubscribeUser
from .tokens import account_activation_token
from .forms import RegisterForm, UserForm, LoginForm, UpdateForm, SubscribeForm
import json
import requests

# Create your views here.

# FUNCTION BASE VIEWS :-

# SUBSCRIBE VIEW :-
data_center = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID
api_key = settings.MAILCHIMP_API_KEY
api_url = f'https://{data_center}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{list_id}/members'


def send_mail(mail_subject, to_email, message):
    try:
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        message = 'success'
        return message
    except:
        message = 'un-success'
        return message


def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    print('data--->', data)
    r = requests.post(
        members_endpoint,
        auth=("", api_key),
        data=json.dumps(data)
    )
    print('r.status_code---->', r.status_code)
    print('r.json()--->', r.json())
    error_msg = r.json()

    return r.status_code, error_msg['errors'][0]['message']


def subscribe_user(request):
    form = SubscribeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and request.is_ajax():
            subscribe_emails = SubscribeUser.objects.filter(email=form.instance.email)
            if subscribe_emails.exists():
                data = {"status": "404"}
                return JsonResponse(data)
            else:
                e = subscribe(form.instance.email)
                print(e)
                if e[0] == 200:
                    form.save()
                data = {"status": e[0],
                        "msg": e[1]}
                return JsonResponse(data)

    return HttpResponseRedirect("/")


# USER REGISTER VIEW :-


def user_register(request):
    user_form = UserForm(request.POST or None)
    profile_form = RegisterForm(request.POST or None)
    if profile_form.is_valid() and user_form.is_valid():
        user = user_form.save(commit=False)
        username = user_form.cleaned_data.get('username')
        password = user_form.cleaned_data.get('password')
        user.is_active = False
        user.set_password(password)
        user.save()
        user_id = User.objects.get(username=username)
        user_profile = profile_form.save(commit=False)
        user_profile.user = user_id
        user_profile.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        to_email = user_form.cleaned_data.get('email')
        message = render_to_string('acc_active_email.html',
                                   {
                                       'user': user,
                                       'domain': current_site,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   })
        resp = send_mail(mail_subject, to_email, message)
        if resp == "success":
            msg = 'Firstly check your Email for activation'
            return render(request, 'confirm_msg.html',
                          {'msg': msg, 'link': 'https://mail.google.com/mail/u/?authuser=user@gmail.com',
                           'name': 'gmail'})
        elif resp == "un-success":
            msg = 'The email account that you tried to reach does not exist. register again'
            return render(request, 'confirm_msg.html',
                          {'msg': msg, 'link': '/userprofile/register/', 'name': 'register'})

    context = {
                'profile_form': profile_form,
                'user_form': user_form,
              }
    return render(request, 'register.html', context)


# EMAIL ACTIVATE VIEW:-


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        msg = 'Thanks for your email confirmation Now you can login your account'
        return render(request, 'confirm_msg.html', {'msg': msg, 'link': '/userprofile/myaccount/', 'name': 'login'})
    else:
        msg = 'Activation link is invalid'
        return render(request, 'confirm_msg.html', {'msg': msg})


# USER LOGIN VIEW :-


def user_login(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect(f"/userprofile/myaccount/")

    context = {'form': form,
               }
    template = 'login.html'
    return render(request, template, context)


# USER LOGOUT VIEW :-


def user_logout(request):
    logout(request)
    return redirect("/")


# USER ACCOUNT VIEW :-

# class MyAccount(LoginRequiredMixin, UpdateView):
#     form_class =


@login_required(login_url="/userprofile/login")
def my_account(request):
    username = request.user.username
    user_info = User.objects.get(username=username)
    profile_info = UserProfile.objects.get(user=user_info)
    user_form = UpdateForm(request.POST or None, instance=user_info)
    profile_form = RegisterForm(request.POST or None, instance=profile_info)
    if profile_form.is_valid() and user_form.is_valid():
        obj = user_form.save(commit=False)
        obj.username = request.user.username
        obj.password = request.user.password
        obj.save()
        profile_form.save()
        return redirect(f"/userprofile/myaccount/")

    context = {'user_form': user_form,
               'profile_form': profile_form,
               }

    return render(request, 'my-account.html', context)


def manage_address(request):
    username = request.user.username
    add_address_form = AddAddressForm(request.POST or None)
    address_qs = ManageAddress.objects.filter(user__username=username)

    context = {
                'add_address_form': add_address_form,
                'address': address_qs
              }
    return render(request, 'manage-address.html', context)


def update_address(request, id):
    username = request.user.username
    user = User.objects.get(username=username)
    address_info = ManageAddress.objects.get(id=id)
    update_address_form = ManageAddressForm(request.POST or None, instance=address_info)
    if request.method == "POST":
        if update_address_form.is_valid() and request.is_ajax:
            add_obj = update_address_form.save(commit=False)
            add_obj.user = user
            add_obj.save()
            return redirect(f"/userprofile/manage-address")
    context = {
                'update_address_form': update_address_form,
                'id': id
             }
    return render(request, 'manage-address.html', context)


def add_address(request):
    username = request.user.username
    user_info = User.objects.get(username=username)
    add_address_form = AddAddressForm(request.POST or None)
    print(add_address_form.is_valid())
    if add_address_form.is_valid() and request.is_ajax:
        add_obj = add_address_form.save(commit=False)
        add_obj.user = user_info
        add_obj.save()
        return JsonResponse({'data': 'success'})
    return JsonResponse({'data': 'error'})


def delete_address(request, user_id):
    qs = ManageAddress.objects.get(id=user_id)
    if request.method == "POST" and request.is_ajax:
        qs.delete()
        return JsonResponse({'data': 'success'})
    return JsonResponse({'data': 'error'})
