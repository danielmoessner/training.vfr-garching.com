# Generated by Django 3.1.6 on 2021-06-04 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_fundamentals_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundamentals',
            name='heading',
        ),
        migrations.RemoveField(
            model_name='fundamentals',
            name='video1',
        ),
        migrations.RemoveField(
            model_name='fundamentals',
            name='video2',
        ),
    ]
