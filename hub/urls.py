from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "hub"

urlpatterns = [
    path("", views.UserDataDashboardView.as_view(), name="home"),
    path(
        "privacy/agreement/", views.accept_privacy_notice, name="accept_privacy_notice"
    ),
    path("login/", views.HubLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="hub:home"), name="logout"),
    path(
        "api/v1/context-profile/",
        views.ContextProfileView.as_view(),
        name="context_profile",
    ),
    path(
        "profiles/library", views.LibraryProfileView.as_view(), name="library_profile"
    ),
    path("profiles/blog", views.BlogProfileView.as_view(), name="blog_profile"),
    path("profiles/hub", views.HubProfileView.as_view(), name="hub_profile"),
    path(
        "profiles/library/edit",
        views.LibraryProfileEditView.as_view(),
        name="library_profile_edit",
    ),
    path(
        "profiles/blog/edit",
        views.BlogProfileEditView.as_view(),
        name="blog_profile_edit",
    ),
    path(
    "audit-logs/download/",
    views.download_audit_log,
    name="download_audit_log",
    ),
]
