# Generated by Django 3.1.6 on 2021-04-17 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0006_auto_20210417_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='phase1',
            field=models.CharField(choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], default='START', max_length=50, verbose_name='Baustein 1 Phase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='phase2',
            field=models.CharField(choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], default='START', max_length=50, verbose_name='Baustein 2 Phase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='phase3',
            field=models.CharField(choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], default='START', max_length=50, verbose_name='Baustein 3 Phase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='phase4',
            field=models.CharField(choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], default='START', max_length=50, verbose_name='Baustein 4 Phase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='phase5',
            field=models.CharField(choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], default='START', max_length=50, verbose_name='Baustein 5 Phase'),
            preserve_default=False,
        ),
    ]
