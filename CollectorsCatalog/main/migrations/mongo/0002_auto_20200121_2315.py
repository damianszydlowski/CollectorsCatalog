# Generated by Django 2.2.9 on 2020-01-21 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectible',
            name='added_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Added at'),
        ),
        migrations.AlterField(
            model_name='collectible',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]