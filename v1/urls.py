from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # restricted allauth links
    path('accounts/', include('hub.allauth_urls')),

    # Hub OAuth provider endpoints
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),

    # Library simulated client app
    path("library/", include("library.urls")),

    path("hub/", include("hub.urls")),

    # Open API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]