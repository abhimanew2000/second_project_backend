# Generated by Django 5.0 on 2024-02-19 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chats',
            name='user',
        ),
    ]
