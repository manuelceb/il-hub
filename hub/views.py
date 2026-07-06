from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.shortcuts import render

def _log_step(step, **data):
    print(f"[IL-Hub step] {step}")
    for key, value in data.items():
        print(f"[IL-Hub step]   {key}: {value}")

def home(request):
    display_name = None
    if request.user and request.user.is_authenticated:
        display_name = request.user.get_full_name() or request.user.email

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
            display_name = self.request.user.get_full_name() or self.request.user.email


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

    # this section will be improved to support more clients and their corresponding contextual data
    if client_name != "library":
        return Response(
            {
                "error": "Unsupported client",
                "client": client_name,
            },
            status=403,
        )

    data = {
        "client": client_name,
        "user": {
            "ilhub_uid": "4474ce18-a74b-467a-99d9-5b084252f8a0",
            "display_name": "My preferred name to use with Library",
            # metadata
            "interests_1": "literature",
            "interests_2": "science",
            "want_research_lectures": True,
        },
    }
    return Response(data)
