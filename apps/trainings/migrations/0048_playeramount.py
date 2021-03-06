# Generated by Django 3.2.9 on 2022-06-21 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0047_filter_show_on_trainings_generator_step_4'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Spieleranzahl')),
            ],
            options={
                'verbose_name': 'Spieleranzahl',
                'verbose_name_plural': 'Spieleranzahlen',
            },
        ),
    ]
