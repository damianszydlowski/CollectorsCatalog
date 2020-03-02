# main/admin.py

from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from mptt.admin import MPTTModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile, Category, VehicleModel, RacingVehicleModel, Book, Watch, Collectible, \
    Event, Notification


# Register your models here.


class UserProfileInline(admin.StackedInline):
    """ Displays an Inline profile update form on an user update view"""

    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('birth_date', 'avatar')


class CustomUserAdmin(UserAdmin):
    """ Configures update view of an user """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'get_birth_date', 'is_moderator']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_moderator',)}),
    )
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        """ Gets inline instances """
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_birth_date(self, instance):
        """ Returns birth date from profile related to user """
        return instance.profile.birth_date

    get_birth_date.short_description = 'Birth Date'


class CollectibleInline(GenericStackedInline):
    model = Collectible
    extra = 0


@register(Collectible)
class CollectibleAdmin(admin.ModelAdmin):
    model = Collectible
    list_display = ['id', 'name', 'producer', 'category']


class BaseAdmin(admin.ModelAdmin):
    inlines = [CollectibleInline]

    def get_producer(self, instance):
        return instance.collectible.get().producer

    get_producer.short_description = 'Producer'


@register(VehicleModel)
@register(RacingVehicleModel)
class CarModelAdmin(BaseAdmin):
    model = VehicleModel
    list_display = ['id', 'get_producer', 'brand', 'model']


@register(Book)
class BookAdmin(BaseAdmin):
    model = Book
    list_display = ['id', 'get_producer', 'author', 'title']


@register(Watch)
class WatchAdmin(BaseAdmin):
    model = Watch
    list_display = ['id', 'get_producer']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register([UserProfile, Event, Notification])
admin.site.register(Category, MPTTModelAdmin)
