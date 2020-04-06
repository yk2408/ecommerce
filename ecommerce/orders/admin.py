from django.contrib import admin
from .models import AddressManage, PaymentDetails, OrdersDetail, Refund, CouponCode, OrderItem

# Register your models here.

admin.site.register(AddressManage)
admin.site.register(PaymentDetails)
admin.site.register(OrdersDetail)
admin.site.register(OrderItem)
admin.site.register(Refund)
admin.site.register(CouponCode)