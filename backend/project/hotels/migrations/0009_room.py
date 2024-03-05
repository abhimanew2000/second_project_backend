# Generated by Django 5.0 on 2024-01-11 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_remove_hotelimage_image_hotelimage_hotel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10)),
                ('capacity', models.PositiveIntegerField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=8)),
                ('amenities', models.TextField()),
                ('room_type', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotels.hotel')),
            ],
        ),
    ]