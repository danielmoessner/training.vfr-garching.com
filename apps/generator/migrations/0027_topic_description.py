# Generated by Django 3.1.6 on 2021-05-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0026_topic_general_or_filters'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.TextField(default='', verbose_name='Beschreibung'),
            preserve_default=False,
        ),
    ]