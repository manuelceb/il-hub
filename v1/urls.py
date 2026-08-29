from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),

    # restricted allauth links
    path('accounts/', include('hub.allauth_urls')),

    # Hub OAuth provider endpoints
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),

    # Library simulated client app
    path("library/", include("library.urls")),

    # Blog simulated client app
    path("blog/", include("blog.urls")),

    # IL-Hub
    path("hub/", include("hub.urls")),

    # Open API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# dynamic url for serving media (profile photo in this case)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]