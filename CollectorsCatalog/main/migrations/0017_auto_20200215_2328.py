# Generated by Django 3.0.2 on 2020-02-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0016_auto_20200215_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='has_event',
            field=models.BooleanField(default=False, verbose_name='Has event'),
        ),
        migrations.AddField(
            model_name='racingcarmodel',
            name='has_event',
            field=models.BooleanField(default=False, verbose_name='Has event'),
        ),
        migrations.AddField(
            model_name='streetcarmodel',
            name='has_event',
            field=models.BooleanField(default=False, verbose_name='Has event'),
        ),
        migrations.AddField(
            model_name='watch',
            name='has_event',
            field=models.BooleanField(default=False, verbose_name='Has event'),
        ),
    ]