# Generated by Django 3.1.6 on 2021-04-14 13:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0026_training_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='difficulty',
            name='stars',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Sterne'),
            preserve_default=False,
        ),
    ]