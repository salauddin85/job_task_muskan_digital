# Generated by Django 5.1 on 2024-11-23 13:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='related_admin',
        ),
        migrations.RemoveField(
            model_name='module',
            name='user',
        ),
        migrations.AddField(
            model_name='module',
            name='user',
            field=models.ManyToManyField(related_name='module', to=settings.AUTH_USER_MODEL),
        ),
    ]