# Generated by Django 3.1.6 on 2021-04-16 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trainings', '0029_training_focus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('and_filters', models.ManyToManyField(blank=True, related_name='or_blocks', to='trainings.TrainingFilter', verbose_name='UND Filter')),
                ('or_filters', models.ManyToManyField(blank=True, related_name='and_blocks', to='trainings.TrainingFilter', verbose_name='ODER Filter')),
            ],
            options={
                'verbose_name': 'Baustein',
                'verbose_name_plural': 'Bausteine',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('or_filters', models.ManyToManyField(blank=True, related_name='topics', to='trainings.TrainingFilter', verbose_name='ODER Filter')),
            ],
            options={
                'verbose_name': 'Thema',
                'verbose_name_plural': 'Themen',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('block1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='structures1', to='generator.block', verbose_name='Baustein 1')),
                ('block2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='structures2', to='generator.block', verbose_name='Baustein 2')),
                ('block3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='structures3', to='generator.block', verbose_name='Baustein 3')),
                ('block4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='structures4', to='generator.block', verbose_name='Baustein 4')),
                ('block5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='structures5', to='generator.block', verbose_name='Baustein 5')),
            ],
            options={
                'verbose_name': 'Trainingsstruktur',
                'verbose_name_plural': 'Trainingsstrukturen',
                'ordering': ['name'],
            },
        ),
    ]
