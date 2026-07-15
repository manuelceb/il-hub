from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .profile_services import get_user_profile

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def context_profile(request):
    
    _log_step(
        "Context profile API view started",
        authenticated=bool(request.user and request.user.is_authenticated),
    )
    access_token = request.auth
    client_name = access_token.application.name if access_token.application else "unknown"

    if client_name == "unknown":
        return Response(
            {
                "error": "Unknown client",
            },
            status=403,
        )
    
    data = get_user_profile(request.user, client_name)
    
    return Response(data)
