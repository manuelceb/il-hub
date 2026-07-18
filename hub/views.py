from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .profile_services import get_user_profile
from .models import ClientRegistry

def _log_step(step, **data):
    print(f"[IL-Hub step] {step}")
    for key, value in data.items():
        print(f"[IL-Hub step]   {key}: {value}")

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



class ContextProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.auth
        application = getattr(access_token, "application", None)

        if application is None:
            raise AuthenticationFailed(
                "Token has no application."
            )
        try:
            registry  = application.client_configuration
        except ClientRegistry.DoesNotExist:
            raise PermissionDenied(
                "This application is not registered for access."
            )

        if not registry .is_active:
            raise PermissionDenied(
                "Profile access is disabled for this application."
            )

        client_name = application.name.strip().lower()
        data = get_user_profile(
            user=request.user,
            client_name=client_name,
            request=request,
        )

        return Response(data)
