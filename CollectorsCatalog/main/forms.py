# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ChoiceField

from .models import CustomUser, UserProfile, Collectible, VehicleModel, RacingVehicleModel, Event, Book, Watch
from .formresolver.choices import FORM_CHOICES


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_moderator')


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('birth_date', 'avatar', 'is_public')
        exclude = ('watchers',)


class CollectibleForm(forms.ModelForm):
    class Meta:
        model = Collectible
        fields = ('producer', 'product_code', 'production_date', 'limited_production', 'photo', 'event')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ('slug',)


class RacingVehicleModelForm(forms.ModelForm):
    class Meta:
        model = RacingVehicleModel
        fields = '__all__'


class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = '__all__'


class ResolveForm(forms.Form):
    form = ChoiceField(choices=FORM_CHOICES)
