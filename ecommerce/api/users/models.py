from django.db import models

# Create your models here.


class Blacklist(models.Model):
    class Meta:
        db_table = 'blacklist'

    token = models.CharField('token', max_length=255, unique=True)