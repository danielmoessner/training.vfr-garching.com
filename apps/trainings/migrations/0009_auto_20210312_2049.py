# Generated by Django 3.1.6 on 2021-03-12 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0008_auto_20210311_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='training',
            old_name='image',
            new_name='image1',
        ),
    ]
