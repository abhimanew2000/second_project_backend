# Generated by Django 5.0 on 2024-01-11 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_remove_hotelimage_hotel_remove_hotelimage_multiimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelimage',
            name='image',
        ),
        migrations.AddField(
            model_name='hotelimage',
            name='hotel',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='multiimage', to='hotels.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelimage',
            name='multiimage',
            field=models.ImageField(default=None, upload_to='hotel_multi_images/'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
