# Generated by Django 3.0.2 on 2020-02-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20200219_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='isRead',
            field=models.BooleanField(default=False),
        ),
    ]
