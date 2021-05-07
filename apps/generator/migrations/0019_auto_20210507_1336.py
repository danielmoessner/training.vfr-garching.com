# Generated by Django 3.1.6 on 2021-05-07 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0044_delete_training'),
        ('users', '0016_auto_20210422_1733'),
        ('generator', '0018_training'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='block1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings1', to='generator.block', verbose_name='Block 1'),
        ),
        migrations.AlterField(
            model_name='training',
            name='block2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings2', to='generator.block', verbose_name='Block 2'),
        ),
        migrations.AlterField(
            model_name='training',
            name='block3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings3', to='generator.block', verbose_name='Block 3'),
        ),
        migrations.AlterField(
            model_name='training',
            name='block4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings4', to='generator.block', verbose_name='Block 4'),
        ),
        migrations.AlterField(
            model_name='training',
            name='block5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainings5', to='generator.block', verbose_name='Block 5'),
        ),
        migrations.AlterField(
            model_name='training',
            name='exercise1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings1', to='trainings.exercise', verbose_name='Übung 1'),
        ),
        migrations.AlterField(
            model_name='training',
            name='exercise2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings2', to='trainings.exercise', verbose_name='Übung 2'),
        ),
        migrations.AlterField(
            model_name='training',
            name='exercise3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings3', to='trainings.exercise', verbose_name='Übung 3'),
        ),
        migrations.AlterField(
            model_name='training',
            name='exercise4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings4', to='trainings.exercise', verbose_name='Übung 4'),
        ),
        migrations.AlterField(
            model_name='training',
            name='exercise5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings5', to='trainings.exercise', verbose_name='Übung 5'),
        ),
        migrations.AlterField(
            model_name='training',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings', to='generator.structure', verbose_name='Trainingsstruktur'),
        ),
        migrations.AlterField(
            model_name='training',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings', to='generator.topic', verbose_name='Thema'),
        ),
        migrations.AlterField(
            model_name='training',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trainings', to='users.usersettings', verbose_name='Nutzer'),
        ),
    ]
