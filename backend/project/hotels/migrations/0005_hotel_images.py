# Generated by Django 5.0 on 2024-01-11 10:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_remove_hotel_multiimage_hotelimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='hotel_multi_images/'), blank=True, default=list, size=None),
        ),
    ]
