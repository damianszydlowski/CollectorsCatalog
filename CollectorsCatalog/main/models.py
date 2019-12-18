# main/models.py

from django.contrib.auth.models import AbstractUser
from djongo import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

# Create your models here.


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


class MetaData(models.Model):
    added_at = models.DateField(default=datetime.now())
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class BasicFields(models.Model):
    producer = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(_('Model / Product Code'), max_length=300, null=True, blank=True)
    production_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='collectibles/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        abstract = True


class CarFields(models.Model):
    brand = models.CharField(_('Brand'), max_length=50)
    model = models.CharField(_('Model'), max_length=50)
    car_year = models.IntegerField(_('Year of car production'))
    color = models.CharField(_('Color'), max_length=30)

    class Meta:
        abstract = True


class RacingCarFields(models.Model):
    event = models.CharField(_('Event Name'), max_length=100)
    event_year = models.IntegerField(_('Event Year'))
    livery = models.CharField(_('Livery'), max_length=30)
    driver = models.CharField(_('Driver'), max_length=60)

    class Meta:
        abstract = True


class RallyRacingCarFields(models.Model):
    co_driver = models.CharField(_('Co-driver'), max_length=60)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

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


class Collectible(models.Model):
    meta_data = models.EmbeddedModelField(
        model_container=MetaData
    )
    basic_fields = models.EmbeddedModelField(
        model_container=BasicFields
    )
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)


class CarModel(Collectible):
    car_fields = models.EmbeddedModelField(model_container=CarFields)

    class Meta:
        abstract = True


class RacingCarModel(CarModel):
    racing_fields = models.EmbeddedModelField(model_container=RacingCarFields)

    class Meta:
        abstract = True


class RallyRacingCarModel(RacingCarModel):
    rally_fields = models.EmbeddedModelField(model_container=RallyRacingCarFields)
