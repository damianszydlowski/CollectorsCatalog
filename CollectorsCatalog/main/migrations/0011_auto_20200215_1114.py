# Generated by Django 3.0.2 on 2020-02-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0010_auto_20200129_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectible',
            name='category',
        ),
        migrations.AddField(
            model_name='collectible',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='collectibles', to='main.Category'),
        ),
    ]
