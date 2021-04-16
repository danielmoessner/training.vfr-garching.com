# Generated by Django 3.1.6 on 2021-03-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favicon', models.ImageField(upload_to='general/', verbose_name='Favicon')),
                ('meta_title', models.CharField(max_length=60, verbose_name='Meta-Titel')),
                ('meta_description', models.CharField(max_length=120, verbose_name='Meta-Beschreibung')),
                ('meta_image', models.ImageField(upload_to='general/', verbose_name='Meta-Bild')),
            ],
            options={
                'verbose_name': 'Allgemein',
            },
        ),
    ]