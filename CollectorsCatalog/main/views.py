# main/views.py

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, UserProfileForm, CustomUserForm, CollectibleForm, EventForm
from .models import Collectible, Category, Event, CustomUser
from .utils import resolve_forms, unpack_category, unpack_collectible_management, notify_user_accepted, \
    notify_users_added


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'profile/signup.html'


@login_required
@transaction.atomic
def profile_update(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profiles was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def moderator_panel(request):
    if not request.user.is_moderator:
        return HttpResponse(_('You have to be moderator to view this page'), status=401)
    collectibles = Collectible.objects.filter(is_accepted=False)
    context = {'collectibles': collectibles}
    return render(request, 'moderator/panel.html', context=context)


@login_required
def moderator_panel_approve(request, collectible_pk):
    if not request.user.is_moderator:
        return HttpResponse(_('You have to be moderator to view this page'), status=401)
    collectible = Collectible.objects.get(id=collectible_pk)
    collectible.is_accepted = True
    collectible.save()
    notify_user_accepted(request.user, collectible.added_by, collectible)
    return redirect('moderator_panel')


@require_http_methods(["GET", "POST"])
def home_page(request):
    recent_collectibles = Collectible.objects.filter(is_accepted=True)[:12]
    popular_collectibles = \
        Collectible.objects.filter(is_accepted=True).annotate(count=Count('owners__id')).order_by('-count')[:12]
    popular_categories = \
        Category.objects.filter(children=None).annotate(count=Count('collectibles__id')).order_by('-count')[:3]
    context = {'recent_collectibles': recent_collectibles,
               'popular_collectibles': popular_collectibles,
               'categories': popular_categories}
    return render(request, 'home.html', context)


class CollectibleDetailView(DetailView):
    model = Collectible
    template_name = 'collectible/detail.html'


@require_http_methods(["GET"])
def search(request):
    """
    Searches for categories (:model:`main.Category`),users (:model:`main.CustomUser`) and
    collectibles (:model:`main.Collectible`)
    """
    query = request.GET.get('q', None)
    category_id = request.GET.get('category', None)
    category = None
    if category_id:
        # if users started search while being on category level view
        # results only contains collectibles matching query within this category and its descendants
        category = Category.objects.get(pk=category_id)
        found_collectibles = Collectible.objects.filter(
            category__in=category.get_descendants(include_self=True),
            name__icontains=query
        )
    else:
        # else findes all collectibles matching the query
        found_collectibles = Collectible.objects.filter(name__icontains=query)
    found_categories = Category.objects.filter(name__icontains=query)
    profiles = get_user_model().objects.filter((Q(first_name__icontains=query) | Q(last_name__icontains=query) |
                                               Q(username__icontains=query)), profile__is_public=True)
    context = {'category': category,
               'found_collectibles': found_collectibles,
               'found_categories': found_categories,
               'found_profiles': profiles,
               }
    return render(request, 'search_results.html', context)


@login_required
def collectible_add(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    base_form = CollectibleForm(request.POST, prefix='base', initial={'producer': 'Minichamps'})
    base_form.fields['producer'].initial = 'Minichamps'
    content_form = resolve_forms(category.form)(request.POST, prefix='content')
    event_form = EventForm(request.POST, prefix='event')
    if request.method == 'POST':
        if base_form.is_valid() and content_form.is_valid() and event_form.is_valid():
            content = content_form.save()
            base = base_form.save(commit=False)
            event = event_form.save()
            base.event = event
            base.category = category
            base.added_by = request.user
            base.added_at = timezone.now()
            name = content_form.Meta.model.generate_name(content, base, event)
            base.name = name
            base.is_accepted = False
            base.content_object = content
            base.save()
            return redirect('home')
    context = {
        'base_form': base_form,
        'content_form': content_form,
        'event_form': event_form,
        'category': category
    }
    return render(request, 'collectible/add.html', context)


def category_index(request):
    return render(request, "category/index.html", {'categories': Category.objects.all()})


def category_show(request, hierarchy=None):
    parent, slug = unpack_category(hierarchy)
    try:
        instance = Category.objects.get(parent=parent, slug=slug)
    except Category.DoesNotExist:
        if slug == 'add':
            return redirect('collectible_add', {'category_slug': parent.slug})
        return redirect('collectible_show', {'slug': slug})
    else:
        collectibles = Collectible.objects.filter(category__in=instance.get_descendants(include_self=True))
        return render(request, 'category/show.html', {'category': instance, 'collectibles': collectibles})


def event_index(request):
    events = Event.objects.all()
    return render(request, 'event/index.html', {'events': events})


def event_show(request, slug):
    event = Event.objects.get(slug=slug)
    collectibles = Collectible.objects.filter(event=event)
    return render(request, 'event/show.html', {'event': event, 'collectibles': collectibles})


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'profile/show.html'


@login_required
def own_collection(request):
    user = request.user
    collectibles = Collectible.objects.filter(owners__in=[user])
    return render(request, 'profile/collection.html', {
        'collectibles': collectibles,
        'is_user_page': True,
    })


@login_required
@require_http_methods("POST")
def ajax_add_to_collection(request):
    user, collectible = unpack_collectible_management(request)
    collectible.owners.add(user)
    collectible.save()
    notify_users_added(user, collectible)
    data = {
        'status': True
    }
    return JsonResponse(data)


@login_required
@require_http_methods("POST")
def ajax_remove_from_collection(request):
    user, collectible = unpack_collectible_management(request)
    collectible.owners.remove(user)
    collectible.save()
    data = {
        'status': True,
        'remove': True
    }
    return JsonResponse(data)


@login_required
@require_http_methods("POST")
def ajax_watch_user(request):
    user = request.user
    target_pk = request.POST.get('target')
    if int(user.pk) == int(target_pk):
        data = {
            'status': False,
            'message': _('You cannot watch yourself!'),
        }
    else:
        target = CustomUser.objects.get(pk=target_pk).profile
        user.profile.observed.add(target)
        user.save()
        data = {
            'status': True,
        }
    return JsonResponse(data)



