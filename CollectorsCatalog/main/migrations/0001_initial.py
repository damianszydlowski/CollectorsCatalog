# Generated by Django 3.0.2 on 2020-01-26 09:44

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                              help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                              max_length=150, unique=True,
                                              validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                              verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_moderator', models.BooleanField(default=False, verbose_name='Moderator')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('cover', models.CharField(choices=[('S', 'Soft'), ('H', 'Hard')], max_length=1)),
                ('genre', models.CharField(max_length=100, verbose_name='Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='main.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('type', models.CharField(choices=[('R', 'Race'), ('W', 'Rally'), ('X', 'Rallycross'), ('W', 'War')],
                                          max_length=1, verbose_name='Type')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Event Name')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Event Year')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Event Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StreetCarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=30, verbose_name='Brand')),
                ('model', models.CharField(max_length=30, verbose_name='Model')),
                ('car_year', models.IntegerField(verbose_name='Production Year')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('scale', models.IntegerField(verbose_name='Scale 1:')),
                ('body_style', models.CharField(
                    choices=[('W', 'Wagon'), ('S', 'Sedan'), ('H', 'Hatchback'), ('C', 'Coupe'), ('T', 'Pickup truck'),
                             ('U', 'SUV')], max_length=1, verbose_name='Body style')),
                ('engine_system', models.CharField(
                    choices=[('I', 'Inline'), ('V', 'V'), ('S', 'Straight'), ('W', 'W'), ('R', 'Rotary'),
                             ('F', 'Flat')], max_length=1, verbose_name='Engine Type (System)')),
                ('engine_cylinders', models.IntegerField(verbose_name='Number of cylinders')),
                ('engine_capacity', models.FloatField(verbose_name='Capacity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mechanism', models.CharField(choices=[('Q', 'Qwartz (Battery)'), ('M', 'Manual (ETA)')], max_length=1,
                                               verbose_name='Mechanism')),
                ('strap', models.CharField(max_length=30, verbose_name='Strap')),
            ],
            options={
                'verbose_name_plural': 'Watches',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=255, null=True, upload_to='avatars/%Y/%m/')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Data urodzenia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RacingCarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=30, verbose_name='Brand')),
                ('model', models.CharField(max_length=30, verbose_name='Model')),
                ('car_year', models.IntegerField(verbose_name='Production Year')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('scale', models.IntegerField(verbose_name='Scale 1:')),
                ('driver', models.CharField(max_length=60, verbose_name='Driver')),
                ('co_driver', models.CharField(blank=True, max_length=60, null=True, verbose_name='Co-driver')),
                ('engine_supplier',
                 models.CharField(blank=True, max_length=60, null=True, verbose_name='Engine Supplier')),
                (
                'tire_supplier', models.CharField(blank=True, max_length=60, null=True, verbose_name='Tires Supplier')),
                ('car_number', models.IntegerField(blank=True, null=True, verbose_name='Car start number')),
                ('car_class', models.CharField(blank=True, max_length=30, null=True, verbose_name='Class')),
                ('position', models.IntegerField(blank=True, null=True, verbose_name='Position')),
                ('series', models.CharField(blank=True, max_length=60, null=True, verbose_name='Series')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Collectible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('producer',
                 models.CharField(blank=True, max_length=40, null=True, verbose_name='Producer / Publishing House')),
                ('product_code',
                 models.CharField(blank=True, max_length=30, null=True, verbose_name='Product Code / Model Number')),
                ('limited_production', models.IntegerField(blank=True, null=True, verbose_name='Limited production')),
                ('production_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='collectibles/%Y/%m/%d/')),
                ('object_id', models.PositiveIntegerField()),
                ('added_at', models.DateField(default=django.utils.timezone.now, verbose_name='Added at')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='Is accepted')),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to=settings.AUTH_USER_MODEL)),
                ('category',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Category')),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
