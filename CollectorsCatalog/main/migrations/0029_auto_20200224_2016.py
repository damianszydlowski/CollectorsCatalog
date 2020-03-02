# Generated by Django 3.0.2 on 2020-02-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20200222_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='watchers',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='watched',
            field=models.ManyToManyField(blank=True, related_name='_userprofile_watched_+', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('ADDED', 'added to his collection item:'), ('ACCEPTED', 'Collectible added by you is accepted'), ('WATCHED', 'added you to his watcn list')], default='ADDED', max_length=20),
        ),
    ]
