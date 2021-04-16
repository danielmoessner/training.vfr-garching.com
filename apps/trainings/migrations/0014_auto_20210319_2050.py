# Generated by Django 3.1.6 on 2021-03-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0013_auto_20210319_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('ordering', models.IntegerField(verbose_name='Sortierung')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Altersgruppe',
                'verbose_name_plural': 'Altersgruppen',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='trainingfilter',
            name='age_group',
            field=models.ManyToManyField(null=True, to='trainings.AgeGroup', verbose_name='Altersgruppe'),
        ),
    ]