# Generated by Django 3.1.6 on 2021-04-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
        ('users', '0015_usersettings_search'),
        ('trainings', '0031_auto_20210416_1445'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrainingFilter',
            new_name='Filter',
        ),
    ]
