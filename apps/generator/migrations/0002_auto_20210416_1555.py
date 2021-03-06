# Generated by Django 3.1.6 on 2021-04-16 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.block')),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.structure')),
            ],
        ),
        migrations.AddField(
            model_name='structure',
            name='blocks',
            field=models.ManyToManyField(through='generator.StructureBlock', to='generator.Block'),
        ),
    ]
