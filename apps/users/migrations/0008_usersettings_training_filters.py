# Generated by Django 3.1.6 on 2021-03-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0019_auto_20210321_1424'),
        ('users', '0007_auto_20210322_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='training_filters',
            field=models.ManyToManyField(blank=True, related_name='users', to='trainings.TrainingFilter'),
        ),
    ]
