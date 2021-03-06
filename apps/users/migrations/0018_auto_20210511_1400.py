# Generated by Django 3.1.6 on 2021-05-11 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0044_delete_training'),
        ('users', '0017_auto_20210511_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='age_group',
            field=models.ForeignKey(blank=True, help_text='Diese Einstellung schränkt die angezeigten Trainings ein.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='trainings.youth', verbose_name='Altersgruppe'),
        ),
    ]
