from .choices import NOTIF_ADDED, NOTIF_ACCEPTED
from .formresolver.choices import *
from .forms import BookForm, RacingVehicleModelForm, VehicleModelForm, WatchForm
from .models import Category, Notification, CustomUser, Collectible

FORMS = {BOOK_FORM: BookForm,
         WATCH_FORM: WatchForm,
         VEHICLE_MODEL_FORM: VehicleModelForm,
         RACING_VEHICLE_MODEL_FORM: RacingVehicleModelForm,
         }


def resolve_forms(form_name):
    return FORMS[form_name]


def unpack_category(hierarchy):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    return parent, category_slug[-1]


def unpack_collectible_management(request):
    user_pk = request.POST.get("user", None)
    collectible_pk = request.POST.get('collectible', None)
    user = CustomUser.objects.get(pk=user_pk)
    collectible = Collectible.objects.get(pk=collectible_pk)
    return user, collectible


def notify_users_added(user, collectible):
    for watcher in user.profile.watchers.all():
        notification = Notification()
        notification.type = NOTIF_ADDED
        notification.sender = user.profile
        notification.receiver = watcher
        notification.collectible = collectible
        notification.save()


def notify_user_accepted(moderator, user, collectible):
    notification = Notification()
    notification.type = NOTIF_ACCEPTED
    notification.sender = moderator.profile
    notification.receiver = user.profile
    notification.collectible = collectible
    notification.save()
