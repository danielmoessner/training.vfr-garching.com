# Generated by Django 3.1.6 on 2021-05-26 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0028_auto_20210524_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='topics', to='generator.group'),
        ),
    ]