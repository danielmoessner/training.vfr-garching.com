# Generated by Django 3.1.6 on 2021-04-26 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0012_auto_20210426_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='structure',
            old_name='block1',
            new_name='blocks1',
        ),
        migrations.AlterField(
            model_name='topic',
            name='structures',
            field=models.ManyToManyField(blank=True, to='generator.Structure', verbose_name='Strukturen'),
        ),
    ]