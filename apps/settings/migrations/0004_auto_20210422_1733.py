# Generated by Django 3.1.6 on 2021-04-22 15:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_general_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='general',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='general',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
