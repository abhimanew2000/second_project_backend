# Generated by Django 5.0 on 2024-01-09 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_hotel_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='multiimage',
            field=models.ImageField(blank=True, null=True, upload_to='hotel_multi_images/'),
        ),
    ]
