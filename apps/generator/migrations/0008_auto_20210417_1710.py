# Generated by Django 3.1.6 on 2021-04-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0007_auto_20210417_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='phase1',
            field=models.CharField(blank=True, choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], max_length=50, null=True, verbose_name='Baustein 1 Phase'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='phase2',
            field=models.CharField(blank=True, choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], max_length=50, null=True, verbose_name='Baustein 2 Phase'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='phase3',
            field=models.CharField(blank=True, choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], max_length=50, null=True, verbose_name='Baustein 3 Phase'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='phase4',
            field=models.CharField(blank=True, choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], max_length=50, null=True, verbose_name='Baustein 4 Phase'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='phase5',
            field=models.CharField(blank=True, choices=[('START', 'Warm-Up'), ('MAIN', 'Hauptteil'), ('END', 'Abschluss')], max_length=50, null=True, verbose_name='Baustein 5 Phase'),
        ),
    ]