from django.contrib import admin
from .models import OrderDetails, ManageAddress, Payment, Coupon, Refund
# Register your models here.

admin.site.register(OrderDetails)
admin.site.register(ManageAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
