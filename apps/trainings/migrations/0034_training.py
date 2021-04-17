# Generated by Django 3.1.6 on 2021-04-16 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
        ('trainings', '0033_auto_20210416_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trainings', to='generator.topic')),
            ],
        ),
    ]