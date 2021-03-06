# Generated by Django 3.0.2 on 2020-02-16 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20200216_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='has_event',
        ),
        migrations.RemoveField(
            model_name='racingcarmodel',
            name='event',
        ),
        migrations.RemoveField(
            model_name='racingcarmodel',
            name='has_event',
        ),
        migrations.RemoveField(
            model_name='streetcarmodel',
            name='has_event',
        ),
        migrations.RemoveField(
            model_name='watch',
            name='has_event',
        ),
        migrations.AddField(
            model_name='collectible',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Event'),
        ),
    ]
