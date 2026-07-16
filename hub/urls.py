from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "hub"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.HubLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="hub:home"), name="logout"),
    path("api/context-profile/", views.ContextProfileView.as_view(), name="context_profile"),
]
