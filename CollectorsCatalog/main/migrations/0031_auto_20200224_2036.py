# Generated by Django 3.0.2 on 2020-02-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20200224_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='observed',
            field=models.ManyToManyField(blank=True, null=True, related_name='_userprofile_observed_+', to='main.UserProfile'),
        ),
    ]