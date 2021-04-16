# Generated by Django 3.1.6 on 2021-04-14 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0026_training_difficulty'),
        ('users', '0010_auto_20210414_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='difficulties',
            field=models.ManyToManyField(blank=True, related_name='users', to='trainings.Difficulty'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='filter_groups',
            field=models.ManyToManyField(blank=True, related_name='users', to='trainings.FilterGroup'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='training_filters',
            field=models.ManyToManyField(blank=True, related_name='users', to='trainings.TrainingFilter'),
        ),
    ]