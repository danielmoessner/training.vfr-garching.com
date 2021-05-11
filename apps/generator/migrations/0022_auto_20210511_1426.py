# Generated by Django 3.1.6 on 2021-05-11 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0044_delete_training'),
        ('generator', '0021_auto_20210511_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='end_or_filters',
            field=models.ManyToManyField(blank=True, related_name='end_topic', to='trainings.Filter', verbose_name='ABSCHLUSS ODER Filter'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='start_or_filters',
            field=models.ManyToManyField(blank=True, related_name='start_topics', to='trainings.Filter', verbose_name='WARM-UP ODER Filter'),
        ),
    ]
