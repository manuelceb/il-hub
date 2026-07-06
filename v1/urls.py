from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Hub OAuth provider endpoints
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),

    # Library simulated client app
    path("library/", include("library.urls")),

    path("hub/", include("hub.urls")),
]