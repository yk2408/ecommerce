# Generated by Django 2.2.7 on 2020-01-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoryandproduct', '0009_auto_20191226_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='electronicproduct',
            name='categories',
            field=models.CharField(blank=True, choices=[('mobiles', 'mobile'), ('laptops', 'laptops'), ('tablets', 'tablets'), ('desktop_pcs', 'pcs')], max_length=20, null=True),
        ),
    ]
