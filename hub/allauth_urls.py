from django.urls import path
from allauth.socialaccount.providers.google import views as google_views

"""
To avoid exposing all django-allauth urls, these are the unique needed for IL-Hub workflow.
"""

urlpatterns = [
    path("google/login/", google_views.oauth2_login, name="google_login",),
    path("google/login/callback/", google_views.oauth2_callback, name="google_callback",),
]