# Generated by Django 3.1.6 on 2021-04-22 15:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_usersettings_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersettings',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
