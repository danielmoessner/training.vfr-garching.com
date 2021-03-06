# Generated by Django 3.1.6 on 2021-05-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0044_delete_training'),
        ('generator', '0025_training_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='general_or_filters',
            field=models.ManyToManyField(blank=True, related_name='general_topics', to='trainings.Filter', verbose_name='ALLGEMEINE ODER Filter'),
        ),
    ]
