# Generated by Django 3.0.2 on 2020-02-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20200224_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='observed',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='main.UserProfile'),
        ),
    ]
