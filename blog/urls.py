from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_with_hub, name="login_with_hub"),
    path("logout/", views.logout_from_blog, name="logout"),
    path("oauth/callback/", views.oauth_callback, name="oauth_callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
