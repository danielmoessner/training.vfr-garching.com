# Generated by Django 3.1.6 on 2021-03-19 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0017_auto_20210319_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingfilter',
            name='age_groups',
            field=models.ManyToManyField(blank=True, to='trainings.AgeGroup', verbose_name='Altersgruppen'),
        ),
    ]
