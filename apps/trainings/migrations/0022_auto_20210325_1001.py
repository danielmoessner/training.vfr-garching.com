# Generated by Django 3.1.6 on 2021-03-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0021_auto_20210324_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='video',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Video'),
        ),
        migrations.AddField(
            model_name='trainingfilter',
            name='show_on_detail',
            field=models.BooleanField(default=False, verbose_name='Auf der Detailseite anzeigen'),
        ),
    ]
