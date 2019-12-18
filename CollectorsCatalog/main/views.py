# main/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django import forms
from django.views.generic.edit import CreateView, UpdateView
from .models import Category, Collectible
from pprint import pprint
from .forms import CustomUserCreationForm, UserProfileForm, CustomUserForm, CollectibleForm
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


def add_collectible(request):
    category = Category.objects.get(id=2)
    category_fields = unpack_fields(category)
    collectible = Collectible()
    if request.method == 'POST':
        form = CollectibleForm(request.POST, instance=collectible, category_fields=category_fields)
        if form.is_valid():
            collectible = form.save()
            d = {}
            for field in category_fields:
                d[field.slug] = form.cleaned_data[field.slug]
            Collectible.objects.mongo_update({"id": collectible.id}, {"$set": d})
            return redirect('collectible_show', collectible_id=collectible.id)
        collectible_form = CollectibleForm(category_fields=category_fields)
        return render(request, 'collectible/new.html', {'form': collectible_form})


def show_collectible(request, collectible_id):
    collectible = Collectible.objects.get(id=collectible_id)
    category = collectible.category
    category_fields = unpack_fields(category)
    brand = collectible.brand
    return render(request, 'collectible/show.html', {'collectible': collectible, 'brand': brand})


def unpack_fields(category):
    category_fields = []
    if category.parent is None:
        return category_fields.all()
    hierarchy = [category]
    p = category.parent
    while p is not None:
        hierarchy.append(p)
        p = p.parent
    hierarchy.reverse()
    for el in hierarchy:
        category_fields += el.fields.all()
    return category_fields


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
