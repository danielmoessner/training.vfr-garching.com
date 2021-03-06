# Generated by Django 3.1.6 on 2021-03-22 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0019_auto_20210321_1424'),
        ('users', '0005_auto_20210321_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='users', to='trainings.FilterGroup'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='age_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='trainings.agegroup'),
        ),
    ]
