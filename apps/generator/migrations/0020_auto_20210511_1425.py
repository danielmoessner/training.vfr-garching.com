# Generated by Django 3.1.6 on 2021-05-11 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0019_auto_20210507_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='warm_up_or_filters',
            new_name='start_or_filters',
        ),
    ]