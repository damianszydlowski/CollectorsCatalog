# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.images import get_image_dimensions

from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_moderator')


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
        fields = ('birth_date', 'avatar', )

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #
    #         # validate dimensions
    #         max_width = max_height = 500
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 'Please use an image that is {} x {} pixels or smaller.'.format(max_width, max_height)
    #             )
    #
    #         # validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')
    #
    #         # validate file size
    #         max_size = 500
    #         if len(avatar) > (max_size * 1024):
    #             raise forms.ValidationError('Avatar file size may not exceed {}kB.'.format(max_size))
    #
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profiles
    #         and do not supply a new avatar
    #         """
    #         pass
    #
    #     return avatar
