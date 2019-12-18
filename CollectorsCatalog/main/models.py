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
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class BasicFields(models.Model):
    producer = models.CharField(max_length=100, null=True, blank=True)
    product_code = models.CharField(_('Product Code / Model Number'), max_length=300, null=True, blank=True)
    production_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='collectibles/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        abstract = True


# *********** Car specific fields start
class CarFields(models.Model):
    brand = models.CharField(_('Brand'), max_length=50)
    model = models.CharField(_('Model'), max_length=50)
    car_year = models.IntegerField(_('Production Year'))
    color = models.CharField(_('Color'), max_length=30)
    scale = models.IntegerField(_('Scale 1:'))

    class Meta:
        abstract = True


class RacingCarFields(models.Model):
    livery = models.CharField(_('Livery'), max_length=30)
    driver = models.CharField(_('Driver'), max_length=60)
    event = models.CharField(_('Event Name'), max_length=100)
    event_year = models.IntegerField(_('Event Year'))
    car_number = models.IntegerField(_('Car start number'))
    position = models.IntegerField(_('Position'), null=True, blank=True)
    series = models.CharField(_('Series'), max_length=60)

    class Meta:
        abstract = True


class RallyRacingCarFields(models.Model):
    co_driver = models.CharField(_('Co-driver'), max_length=60, null=True, blank=True)


class F1RacingCarFields(models.Model):
    engine_supplier = models.CharField(_('Engine Supplier'), max_length=60)
    tire_supplier = models.CharField(_('Tires Supplier'), max_length=60)
# *********** Car specific fields end


class Collectible(models.Model):
    meta_data = models.EmbeddedModelField(
        model_container=MetaData
    )
    basic_fields = models.EmbeddedModelField(
        model_container=BasicFields
    )
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        # return str(self.id)
        s = self.basic_fields.producer
        if self.basic_fields.product_code is not None:
            s += ' ' + self.basic_fields.product_code
        else:
            s += ' ' + self.id
        return s


class CarModel(Collectible):
    car_fields = models.EmbeddedModelField(model_container=CarFields)

    class Meta:
        abstract = True


class RacingCarModel(CarModel):
    racing_fields = models.EmbeddedModelField(model_container=RacingCarFields)
    objects = models.DjongoManager()


class RallyRacingCarModel(RacingCarModel):
    rally_fields = models.EmbeddedModelField(model_container=RallyRacingCarFields)
    objects = models.DjongoManager()


class F1RacingCarModel(RacingCarModel):
    f1_fields = models.EmbeddedModelField(model_container=F1RacingCarFields)
    objects = models.DjongoManager()