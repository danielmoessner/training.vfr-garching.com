# Generated by Django 3.1.6 on 2021-06-04 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0031_topic_pre'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='description',
            field=models.TextField(default='lorem ipsum dolor sit amet. Das ist ein Beispieltext zum testen.', verbose_name='Beschreibung'),
            preserve_default=False,
        ),
    ]
