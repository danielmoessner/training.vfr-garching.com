# Generated by Django 3.2.9 on 2022-06-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0037_topic_or_filters_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='exercise_amount',
            field=models.CharField(blank=True, choices=[('3', '3'), ('4', '4'), ('5', '5')], max_length=1, null=True, verbose_name='Übungsanzahl'),
        ),
    ]
