# Generated by Django 3.1.6 on 2021-04-14 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0028_auto_20210414_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='focus',
            field=models.CharField(blank=True, max_length=50, verbose_name='Fokus'),
        ),
    ]
