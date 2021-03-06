from django.urls import path
from . import views


urlpatterns = [
                path('apply-coupon', views.apply_coupon, name="apply-coupon"),
                path('order-item', views.order_details, name="order-item"),
                path('payment-page', views.payment_page, name="payment"),
                path('send-payment', views.send_payment, name='send-payment')
                ]
