# Generated by Django 3.1.6 on 2021-05-11 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_trainings'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainings',
            name='step1_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Schritt 1 Überschrift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainings',
            name='step2_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Schritt 2 Überschrift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainings',
            name='step3_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Schritt 3 Überschrift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainings',
            name='step4_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Schritt 4 Überschrift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainings',
            name='step5_heading',
            field=models.CharField(default='', max_length=100, verbose_name='Schritt 5 Überschrift'),
            preserve_default=False,
        ),
    ]
