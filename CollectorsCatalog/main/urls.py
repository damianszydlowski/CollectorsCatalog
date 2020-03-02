# main/urls.py
from django.conf.urls import url
from django.urls import path

from .views import SignUpView, CollectibleDetailView, moderator_panel, \
    category_index, moderator_panel_approve, category_show, event_index, event_show, \
    search, ajax_add_to_collection, ajax_remove_from_collection, UserDetailView, collectible_add, \
    profile_update, own_collection, ajax_watch_user

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", profile_update, name="profile_update"),
    path("profile/my-collection/", own_collection, name="own_collection"),
    path("profile/<int:pk>", UserDetailView.as_view(), name='profile_show'),

    path("moderator-panel/", moderator_panel, name="moderator_panel"),

    path("moderator-panel/<int:collectible_pk>", moderator_panel_approve, name="moderator_panel_approve"),

    path("category/", category_index, name="category_index"),
    url(r'^category/(?P<hierarchy>.+)/$', category_show, name='category_show'),
    path("search/", search, name="collectible_search"),
    path("collectible/add/<slug:category_slug>", collectible_add, name="collectible_add"),
    path("collectible/<slug:slug>", CollectibleDetailView.as_view(), name="collectible_show"),
    path("event/", event_index, name='event_index'),
    path("event/<slug:slug>", event_show, name='event_show'),
    path("ajax/add-to-collection", ajax_add_to_collection, name="ajax_add_to_collection"),
    path("ajax/remove-from-collection", ajax_remove_from_collection, name="ajax_remove_from_collection"),
    path("ajax/watch-user", ajax_watch_user, name="ajax_watch_user"),
]
