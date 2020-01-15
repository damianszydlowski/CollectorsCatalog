# main/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile, Category, RacingCarModel, RallyRacingCarModel, \
    F1RacingCarModel, Book, Watch, Collectible


# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('birth_date', 'avatar')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'get_birth_date']
    list_select_related = ('profile',)
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_birth_date(self, instance):
        return instance.profile.birth_date

    get_birth_date.short_description = 'Birth Date'


class CollectibleAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_producer', 'get_product_code']

    def get_producer(self, instance):
        return instance.collectible.producer

    def get_product_code(self, instance):
        return instance.collectible.product_code

    get_producer.short_description = 'Producer'
    get_product_code.short_description = 'Product Code'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register([UserProfile, Category])
admin.site.register([RacingCarModel, RallyRacingCarModel, F1RacingCarModel, Book, Watch], CollectibleAdmin)
