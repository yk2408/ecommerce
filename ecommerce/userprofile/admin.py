from django.contrib import admin
from .models import UserProfile, SubscribeUser

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(SubscribeUser)
