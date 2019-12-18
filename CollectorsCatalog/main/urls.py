# main/urls.py

from django.urls import path
from .views import SignUpView, ProfileUpdate, add_collectible, show_collectible

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdate.as_view(), name="profile_update"),
    path('collectible/add/', add_collectible, name="collectible_add"),
    path('collectible/<collectible_id>/', show_collectible, name="collectible_show"),
]
