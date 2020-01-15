# main/views.py
from urllib.request import Request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django import forms
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView

from .models import Collectible, RallyRacingCarModel
from .forms import CustomUserCreationForm, UserProfileForm, CustomUserForm
from django.utils.translation import ugettext_lazy as _


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'profiles/signup.html'


class ProfileUpdate(UpdateView):
    fields = ['birthDate', 'avatar']
    template_name = 'profiles/edit.html'
    success_url = reverse_lazy('profile_update')

    def get_object(self):
        return self.request.user.profile


@require_http_methods(["GET", "POST"])
def home_page(request):
    # entries = Entry.objects.filter(blog={'name': 'Beatles Blog'})
    collectibles = RallyRacingCarModel.objects.filter(collectible={'producer': 'Minichamps'})
    # producers = RallyRacingCarModel.objects.basic_fields('producer')
    context = {'collectibles': collectibles}
    return render(request, 'home.html', context)

# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = CustomUserForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profiles was successfully updated!'))
#             return redirect('settings:profiles')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = CustomUserForm(instance=request.user)
#         profile_form = UserProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/edit.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
