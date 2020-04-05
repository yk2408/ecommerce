from django.contrib import admin
from .models import CartItem, WishList

# Register your models here.

admin.site.register(CartItem)
admin.site.register(WishList)
