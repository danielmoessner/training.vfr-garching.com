# Generated by Django 3.1.6 on 2021-04-16 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_auto_20210416_1608'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ['name'], 'verbose_name': 'Struktur', 'verbose_name_plural': 'Strukturen'},
        ),
    ]
