from django.conf import settings
from django.db import models
from cart.models import CartItem
from django_countries.fields import CountryField
from categoryandproduct.models import ElectronicProduct
from datetime import datetime
# Create your models here.

ADDRESS_TYPES = (
    ('Home', 'home'),
    ('Work', 'work'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


ORDER_STATUS = (
    ('Delivered', 'delivered'),
    ('Cancelled', 'cancelled'),
    ('Processing', 'processing'),
    ('Ordered', 'ordered'),
    ('Packed', 'packed'),
    ('Shipped', 'shipped'),
    ('Pending', 'pending'),
    ('Transaction Failed', 'transaction failed')
)
state_choices = (
        ("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"),
        ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"), ("Jammu and Kashmir ", "Jammu and Kashmir "),
        ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"), ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"), ("Odisha", "Odisha"), ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"),
        ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"),
        ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"),
        ("Lakshadweep", "Lakshadweep"), ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
        ("Puducherry", "Puducherry"))


class AddressManage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=12)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=20)
    state = models.CharField(choices=state_choices, max_length=20)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)

    def __str__(self):
        return str(self.pk) + self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class OrderAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=12)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=20)
    state = models.CharField(choices=state_choices, max_length=20)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)

    def __str__(self):
        return str(self.pk) + self.user.username


class PaymentDetails(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class CouponCode(models.Model):
    code = models.CharField(max_length=15)
    code_title = models.CharField(max_length=255, null=True, blank=True)
    code_description = models.TextField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    order_above = models.FloatField(null=True, blank=True)
    validation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


class OrdersDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS, default="Processing", null=True, max_length=20, blank=True)
    shipping_address = models.ForeignKey(
        'OrderAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'OrderAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'PaymentDetails', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'CouponCode', on_delete=models.SET_NULL, blank=True, null=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(ElectronicProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(OrdersDetail, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS, default="Ordered", null=True, max_length=20, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == "Delivered":
            self.delivered_date = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    @property
    def total(self):
        return self.quantity * self.price


class Refund(models.Model):
    order = models.ForeignKey(OrdersDetail, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
