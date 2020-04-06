from django import forms
from django.shortcuts import render

# Create your views here.
from .models import AddressManage


class ManageAddressForm(forms.ModelForm):
    CHOICES = [('Home', 'home'), ('Work', 'work')]
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'info'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'info'}))
    mobile_no = forms.IntegerField(widget=forms.TextInput(
            attrs={'placeholder': 'Mobile Number', 'class': 'info'}))
    zip_code = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': 'Zip Code', 'class': 'info'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'City/District/Town', 'class': 'info'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address(Area and Street)', 'class': 'info', 'style': 'height: 160px;'}))
    address_type = forms.CharField(widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'info'}))

    class Meta:
        model = AddressManage
        fields = '__all__'
        exclude = ('user',)


class AddAddressForm(forms.ModelForm):
    CHOICES = [('Home', 'Home'), ('Work', 'Work')]
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'info'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'info'}))
    mobile_no = forms.IntegerField(widget=forms.TextInput(
            attrs={'placeholder': 'Mobile Number', 'class': 'info'}))
    zip_code = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': 'Zip Code', 'class': 'info'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'City/District/Town', 'class': 'info'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address(Area and Street)', 'class': 'info', 'style': 'height: 160px;'}))
    address_type = forms.CharField(widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'info'}))

    class Meta:
        model = AddressManage
        fields = '__all__'
        exclude = ('user',)


class CouponCode(forms.ModelForm):
    class Meta:
        model = AddressManage
        fields = '__all__'

