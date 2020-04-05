from datetime import datetime
from django.db import models
from django.utils.text import slugify
import random

# Create your models here.
ELECTRONIC_CATEGORIES = [('mobiles', 'mobiles'),
                         ('laptops', 'laptops'),
                         ('tablets', 'tablets'),
                         ('pcs', 'pcs')
                         ]


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)


class ElectronicProduct(models.Model):
    product_image = models.ImageField(upload_to='pics')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    special_price = models.FloatField()
    ram = models.CharField(max_length=100)
    rom = models.CharField(max_length=100,)
    expandable_memory = models.CharField(max_length=100, null=True, blank=True)
    display_details = models.CharField(max_length=255)
    processor_details = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)
    warranty = models.CharField(max_length=255)
    color = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    full_description = models.TextField()
    sort_description = models.TextField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
    categories = models.CharField(max_length=20, choices=ELECTRONIC_CATEGORIES, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        random_no = str(random.randint(100, 2000))
        self.slug = slugify(str(self.name)+ random_no)
        super().save(*args, **kwargs)


class SubCategoryMenu(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)


class Product(models.Model):
    electronic_product = models.ForeignKey('ElectronicProduct', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.electronic_product)

