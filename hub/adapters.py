from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class ExistingUserAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


# users/adapters.py

from urllib.parse import urlencode

from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class ExistingUserSocialAccountAdapter(
    DefaultSocialAccountAdapter
):
    """
    Allow Google authentication only for existing IL-Hub users.
    """

    def is_open_for_signup(self, request, sociallogin):
        messages.error(
            request,
            (
                "Google sign-in could not be completed. "
                "Use a Google account already registered with IL-Hub."
            ),
        )

        login_url = reverse("hub:login")

        # Preserve the original destination, such as /o/authorize/.
        next_url = sociallogin.get_redirect_url(request)

        if next_url:
            query_string = urlencode({"next": next_url})
            login_url = f"{login_url}?{query_string}"

        raise ImmediateHttpResponse(
            redirect(login_url)
        )