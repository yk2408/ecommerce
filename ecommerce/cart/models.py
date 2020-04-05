from django.contrib.auth.models import User
from django.db import models
from categoryandproduct.models import Product, Category, ElectronicProduct
from datetime import datetime
from django.conf import settings

# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ElectronicProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username + " " + self.product.name


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(ElectronicProduct, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
