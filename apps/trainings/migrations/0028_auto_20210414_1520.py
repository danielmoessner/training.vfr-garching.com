# Generated by Django 3.1.6 on 2021-04-14 13:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0027_difficulty_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='difficulty',
            name='stars',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)], verbose_name='Sterne'),
        ),
    ]