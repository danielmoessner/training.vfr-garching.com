# Generated by Django 3.2.9 on 2022-07-01 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0054_alter_exercise_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['ordering'], 'verbose_name': 'Filtergruppe', 'verbose_name_plural': 'Filtergruppen'},
        ),
    ]
