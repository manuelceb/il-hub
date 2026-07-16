from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
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



class ContextProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.auth
        client_id = access_token.application.client_id

        if client_id is None:
            raise AuthenticationFailed(
                "The token is not associated with an application."
            )

        data = get_user_profile(
            user=request.user,
            client_id=client_id,
        )

        return Response(data)
