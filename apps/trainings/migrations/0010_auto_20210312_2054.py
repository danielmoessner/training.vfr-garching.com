# Generated by Django 3.1.6 on 2021-03-12 19:54

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0009_auto_20210312_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='coaching',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Coachingpunkte'),
        ),
        migrations.AddField(
            model_name='training',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='training/', verbose_name='Bild'),
        ),
        migrations.AddField(
            model_name='training',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='training/', verbose_name='Bild'),
        ),
        migrations.AddField(
            model_name='training',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='training/', verbose_name='Bild'),
        ),
        migrations.AddField(
            model_name='training',
            name='variations',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Variationen'),
        ),
        migrations.AlterField(
            model_name='training',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Beschreibung'),
        ),
    ]
