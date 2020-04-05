from django import forms
from cart.models import CartItem, WishList


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'


class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = '__all__'
