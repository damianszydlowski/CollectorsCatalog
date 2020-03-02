# main/models.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from . import choices
from .formresolver.choices import FORM_CHOICES, BOOK_FORM


# Create your models here


class CustomUser(AbstractUser):
    """This class extends default auth user model"""
    is_moderator = models.BooleanField(_('Moderator'), default=False)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """This class holds user informations which are not related to authorization"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', max_length=255, blank=True, null=True)
    birth_date = models.DateField(_('Birth date'), blank=True, null=True)
    is_public = models.BooleanField(_('Is Public'), default=True)
    observed = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='watchers')

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """Here's created new user profile everytime when new auth user is created"""

        if created:
            UserProfile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.username


class SluggableModel(models.Model):
    """This is abstract class which defines sluggable behavior for default :model:`django.db.Model`"""
    class Meta:
        abstract = True

    slug = models.SlugField(max_length=100, blank=True)

    def _get_unique_slug(self):
        """
        This method generates and returns an unique slug

        If slug generated by slugify is not unique, it appends a number to it.
        """

        slug = slugify(str(self))
        unique_slug = slug
        num = 1
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Category(MPTTModel, SluggableModel):
    """Category model

    It inherits from MPTTModel and :model:`main.SluggableModel` classes.
    Main purpose is to hold hierarchy of categories inside a project
    """

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True)
    form = models.CharField(max_length=50, choices=FORM_CHOICES, default=BOOK_FORM)

    def __str__(self):
        return self.name

    def get_full_name(self):
        """Returns string with names of category and all it's ancestors in ascending order"""
        ancestors = self.get_ancestors(ascending=True, include_self=True)
        return ' '.join([i.name for i in ancestors])

    def get_breadcrumb(self):
        """Returns string with names of category and all it's ancestors in form of breadcrumbs"""
        ancestors = self.get_ancestors(include_self=True)
        return ' > '.join([i.name for i in ancestors])

    def get_slug_list(self):
        """Returns list of full hierarchy slug for each hierarchy item"""
        try:
            ancestors = self.get_ancestors(include_self=True)
        except ValueError:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs


class Event(SluggableModel):
    """Class which inherits :model:`main.SluggableModel` behavior and defines Event related fields"""
    type = models.CharField(_('Type'), choices=choices.EVENT_TYPES, max_length=1)
    name = models.CharField(_('Event Name'), max_length=100)
    year = models.IntegerField(_('Event Year'))
    country = models.CharField(_('Event Country'), max_length=100)

    def __str__(self):
        return self.type + " " + self.name + " " + str(self.year)


class Collectible(SluggableModel):
    """Collectible """
    name = models.CharField(_('Name'), max_length=255)
    producer = models.CharField(_('Producer / Publishing House'), max_length=40)
    product_code = models.CharField(_('Product Code / Model Number'), max_length=30, blank=True, null=True)
    limited_production = models.IntegerField(_('Limited production'), blank=True, null=True)
    production_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='collectibles/%Y/%m/%d/', blank=True, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='collectibles')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    added_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name='added')
    added_at = models.DateField(_('Added at'), default=now)
    is_accepted = models.BooleanField(_('Is accepted'), default=False)
    owners = models.ManyToManyField(get_user_model(), through='PrivateCollection', related_name='collection')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class DetailedCollectible(models.Model):
    class Meta:
        abstract = True

    def get_all_fields(self):
        fields = []
        for f in self._meta.fields:
            fname = f.name
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except AttributeError:
                    value = None

            if f.editable and value and f.name not in ('id', 'event', 'has_event'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )
        return fields

    def generate_name(self, collectible, event):
        raise NotImplementedError


class PrivateCollection(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='profile_collection', on_delete=models.CASCADE)
    collectible = models.ForeignKey(Collectible, related_name='profile_collection', on_delete=models.CASCADE)
    price = models.FloatField(_('Cena'), blank=True, null=True)
    bought_at = models.DateField(_('Got at'), blank=True, null=True)


class Notification(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='notifications_send', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='notifications', on_delete=models.CASCADE)
    collectible = models.ForeignKey(Collectible, blank=True, null=True, related_name='notifications', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=choices.NOTIFICATION_TYPE_CHOICES, default=choices.NOTIF_ADDED)
    is_read = models.BooleanField(default=False)


class AbstractVehicleModel(models.Model):
    class Meta:
        abstract = True

    brand = models.CharField(_('Brand'), max_length=30)
    model = models.CharField(_('Model'), max_length=30)
    car_year = models.IntegerField(_('Production Year'))
    color = models.CharField(_('Color'), max_length=30)
    scale = models.IntegerField(_('Scale 1:'))
    body_style = models.CharField(_('Body style'), max_length=1, choices=choices.STREET_CAR_MODEL_BODY_CHOICES)
    engine_system = models.CharField(_('Engine Type (System)'), choices=choices.STREET_CAR_MODEL_ENGINE_TYPE_CHOICES,
                                     max_length=1)
    engine_cylinders = models.IntegerField(_('Number of cylinders'))
    engine_capacity = models.FloatField(_('Capacity (cm3)'))
    wheels_number = models.IntegerField(_('Wheels number'), default=4)

    def __str__(self):
        return " ".join([str(self.car_year), self.brand, self.model])


class VehicleModel(AbstractVehicleModel, DetailedCollectible):
    collectible = GenericRelation(Collectible, related_query_name='car_models', on_delete=models.CASCADE)

    def generate_name(self, collectible, event):
        return " ".join([
            "1:{}".format(self.scale), collectible.producer, self.brand,
            self.model, self.color, "({})".format(str(event))])


class RacingVehicleModel(AbstractVehicleModel, DetailedCollectible):
    collectible = GenericRelation(Collectible, related_query_name='racing_car_models', on_delete=models.CASCADE)
    driver = models.CharField(_('Driver'), max_length=60)
    co_driver = models.CharField(_('Co-driver'), max_length=60, blank=True, null=True)
    engine_supplier = models.CharField(_('Engine Supplier'), max_length=60, blank=True, null=True)
    tire_supplier = models.CharField(_('Tires Supplier'), max_length=60, blank=True, null=True)
    car_number = models.IntegerField(_('Car start number'), blank=True, null=True)
    car_class = models.CharField(_('Class'), max_length=30, blank=True, null=True)
    position = models.IntegerField(_('Position'), blank=True, null=True)
    series = models.CharField(_('Series'), max_length=60, blank=True, null=True)

    def generate_name(self, collectible, event):
        return " ".join([
            "1:{}".format(self.scale), collectible.producer, self.brand,
            self.model, self.color, "#{}".format(self.car_number), "({}: {})".format(self.driver, str(event))])


class Book(DetailedCollectible):
    collectible = GenericRelation(Collectible, related_query_name='books', on_delete=models.CASCADE)
    author = models.CharField(_('Author'), max_length=100)
    title = models.CharField(_('Title'), max_length=255)
    cover = models.CharField(_('Cover'), choices=choices.BOOK_COVER_CHOICES, max_length=1)

    def generate_name(self, collectible, event=None):
        return " ".join([
            collectible.producer, "{}:".format(self.author),
            self.title, "({})".format(self.get_cover_display())])


class Watch(DetailedCollectible):
    class Meta:
        verbose_name_plural = 'Watches'

    collectible = GenericRelation(Collectible, related_query_name='watches', on_delete=models.CASCADE)
    mechanism = models.CharField(_('Mechanism'), choices=choices.WATCH_MECHANISM_CHOICES, max_length=1)
    strap = models.CharField(_('Strap'), max_length=30)
