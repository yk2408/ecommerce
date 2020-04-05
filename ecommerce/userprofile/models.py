from django.contrib.auth.models import User
from django.db import models

# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    mobile_number = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile', null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class SubscribeUser(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)
