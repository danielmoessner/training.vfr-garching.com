# Generated by Django 3.2.9 on 2022-06-21 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0033_auto_20220621_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='structures',
        ),
        migrations.RemoveField(
            model_name='training',
            name='block1',
        ),
        migrations.RemoveField(
            model_name='training',
            name='block2',
        ),
        migrations.RemoveField(
            model_name='training',
            name='block3',
        ),
        migrations.RemoveField(
            model_name='training',
            name='block4',
        ),
        migrations.RemoveField(
            model_name='training',
            name='block5',
        ),
        migrations.RemoveField(
            model_name='training',
            name='structure',
        ),
    ]