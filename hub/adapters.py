from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from urllib.parse import urlencode
from allauth.core.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class ExistingUserAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class ExistingUserSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Extracting picture from Google profile recevied. 
        Storing only strictly required data, aligned with GDPR principles.
        """
        extra_data = sociallogin.account.extra_data
        extra_data.pop('picture', None)
        sociallogin.account.extra_data = extra_data

    def is_open_for_signup(self, request, sociallogin):
        """
        Allow Google authentication only for existing IL-Hub users.
        """

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

    def on_authentication_error(
        self,
        request,
        provider,
        error=None,
        exception=None,
        extra_context=None,
    ):
        """
        Custom error handling when user cannot be authenticated 
        (The user possibly refuses agreement on Google's webpage)
        """
        messages.error(
            request,
            "Google authentication could not be completed.",
        )

        raise ImmediateHttpResponse(
            redirect("hub:login")
         )