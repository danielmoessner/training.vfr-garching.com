# Generated by Django 3.1.6 on 2021-04-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210415_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='search',
            field=models.CharField(blank=True, max_length=100, verbose_name='Suche'),
        ),
    ]
