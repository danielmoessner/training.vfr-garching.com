# Generated by Django 3.1.6 on 2021-04-26 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0013_auto_20210426_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='structure',
            old_name='block2',
            new_name='blocks2',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='block3',
            new_name='blocks3',
        ),
    ]