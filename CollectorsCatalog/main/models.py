# main/models.py

from datetime import datetime
from djongo import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from . import model_fields


# Create your models here


class CustomUser(AbstractUser):
    # add additional fields in here
    is_moderator = models.BooleanField(_('Moderator'), default=False)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', max_length=255, null=True, blank=True)
    birth_date = models.DateField(_('Data urodzenia'), blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.profile.save()

        def __str__(self):
            return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent is None:
            return self.name
        # return "{} > {}".format(self.parent.name, self.name)
        hierarchy = [self.name]
        p = self.parent
        while p is not None:
            hierarchy.append(p.name)
            p = p.parent
        s = ""
        hierarchy.reverse()
        for el in hierarchy:
            s = s + el + ' > '
        s = s[:-3]
        return s


class MetaData(models.Model):
    added_at = models.DateField(default=datetime.now())
    is_accepted = models.BooleanField(_('Is accepted'), default=False)

    class Meta:
        abstract = True


class Collectible(models.Model):
    objects = InheritanceManager()
    added_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    meta_data = models.EmbeddedField(
        model_container=MetaData
    )
    photo = models.ImageField(upload_to='collectibles/%Y/%m/%d/', null=True, blank=True)
    collectible = models.EmbeddedField(
        model_container=model_fields.BasicFields
    )
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        # return str(self.id)
        s = self.collectible.producer
        if self.collectible.product_code is not None:
            s += ' ' + self.collectible.product_code
        else:
            s += ' ' + str(self.id)
        return s

    class Meta:
        abstract = True


class CarModel(Collectible):
    car = models.EmbeddedField(model_container=model_fields.CarFields)

    class Meta:
        abstract = True


class RacingCarModel(CarModel):
    race = models.EmbeddedField(model_container=model_fields.RacingCarFields)
    objects = models.DjongoManager()


class RallyRacingCarModel(RacingCarModel):
    rally = models.EmbeddedField(model_container=model_fields.RallyRacingCarFields)
    objects = models.DjongoManager()


class F1RacingCarModel(RacingCarModel):
    f1 = models.EmbeddedField(model_container=model_fields.F1RacingCarFields)
    objects = models.DjongoManager()


class Book(Collectible):
    book = models.EmbeddedField(model_container=model_fields.BookFields)
    objects = models.DjongoManager()


class Watch(Collectible):
    watch = models.EmbeddedField(model_container=model_fields.WatchFields)
    objects = models.DjongoManager()

    class Meta:
        verbose_name_plural = 'Watches'
