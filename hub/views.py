from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .profile_services import get_user_profile
from oauth2_provider.contrib.rest_framework import OAuth2Authentication,TokenHasScope
from .models import ClientRegistry
from .api_errors import ClientInactive, TokenClientError, ClientNotRegistered


def home(request):
    display_name = None
    if request.user and request.user.is_authenticated:
        display_name = request.user.email
    return render(
        request,
        "hub/home.html",
        {
            "display_name": display_name,

        },
    )

class HubLoginView(LoginView):
    template_name = "hub/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_name = None
        if self.request.user and self.request.user.is_authenticated:
            display_name = self.request.user.email
            
        context["display_name"] = display_name
        return context



from .logging_services.events import EventType
from .logging_services.logging_service import record_gdpr_log_event   

class ContextProfileView(APIView):
    
    http_method_names = ["get"]
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["contextual_profile:read"]

    def get(self, request):
        access_token = request.auth
        application = getattr(access_token, "application", None)

        if application is None:
            raise TokenClientError()
        try:
            registry = application.client_configuration
        except ClientRegistry.DoesNotExist:
            raise ClientNotRegistered()

        if not registry.is_active:
            raise ClientInactive()

        client_name = application.name
        data = get_user_profile(
            user=request.user,
            client_name=client_name,
            request=request,
        )

        user_reference = str(request.user.user_uid)
        record_gdpr_log_event(
            event_type=EventType.CONTEXT_PROFILE_ACCESSED,
            outcome="success",
            actor_type= "oauth_client",
            actor_reference=client_name,
            subject_reference=user_reference,
            client_reference=client_name,
        )

        return Response(data)
