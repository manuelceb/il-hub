import secrets
import base64
import hashlib
from urllib.parse import urlencode
import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

def _clear_blog_oauth_session(request):
    # it clears Blog OAuth values from session
    for session_key in (
        "blog_access_token",
        "blog_refresh_token",
        "blog_token_type",
        "blog_scope",
        "blog_oauth_state",
        "blog_oauth_code_verifier",
    ):
        request.session.pop(session_key, None)

def _get_context_profile(access_token):
    if not access_token:
        return None, None, False
  
    # When using bearer tokens, RFC6749 states the following header format to make the request
    response = requests.get(
        settings.HUB_CONTEXT_PROFILE_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    if response.status_code == 200:
        # IL-Hub context profile request succeeded
        context_profile = response.json()
        return context_profile, None, True
    
    return None, response.text, False


def landing(request):
    access_token = request.session.get("blog_access_token")
    context_profile, error, token_is_valid = _get_context_profile(access_token)
    # clearing the django session if token is no longer valid
    if access_token and not token_is_valid:
        _clear_blog_oauth_session(request)
        access_token = None

    return render(
        request,
        "blog/landing.html",
        {
            "is_logged_in": bool(access_token and token_is_valid),
            "context_profile": context_profile,
            "error": error,
        },
    )


def login_with_hub(request):
    # generating PKCE values
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    
    # code challenge should be hashed according to oauth.toolkit blog
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()
    
    # storing OAuth state and code verifier in session
    request.session["blog_oauth_state"] = state
    request.session["blog_oauth_code_verifier"] = code_verifier

    params = {
        "response_type": "code",
        "client_id": settings.BLOG_CLIENT_ID,
        "redirect_uri": settings.BLOG_REDIRECT_URI,
        "scope": "contextual_profile:read",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    # redirecting user to IL-Hub authorize endpoint
    authorize_url = f"{settings.HUB_AUTHORIZE_URL}?{urlencode(params)}"

    return redirect(authorize_url)


def oauth_callback(request):
    
    oauth_error = request.GET.get("error")
    error_description = request.GET.get("error_description")
    code = request.GET.get("code")
    state = request.GET.get("state")

    expected_state = request.session.get("blog_oauth_state")
    code_verifier = request.session.get("blog_oauth_code_verifier")

    if oauth_error:
        message = error_description or oauth_error
        return HttpResponseBadRequest(f"OAuth authorization failed: {message}")

    if not code:
        return HttpResponseBadRequest("Missing authorization code.")

    if not state or state != expected_state:
        return HttpResponseBadRequest("Invalid OAuth state.")

    if not code_verifier:
        return HttpResponseBadRequest("Missing OAuth code verifier.")

    # once callback validated authorization code and state, now it exchanges authorization code for tokens
    response = requests.post(
        settings.HUB_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.BLOG_REDIRECT_URI,
            "client_id": settings.BLOG_CLIENT_ID,
            "client_secret": settings.BLOG_CLIENT_SECRET,
            "code_verifier": code_verifier,
        },
        timeout=10,
    )

    if response.status_code != 200:
        return HttpResponseBadRequest(response.text)

    token_data = response.json()

    # storing tokens in session and cleared temporary OAuth values
    request.session["blog_access_token"] = token_data.get("access_token")
    request.session["blog_refresh_token"] = token_data.get("refresh_token")
    request.session["blog_token_type"] = token_data.get("token_type")
    request.session["blog_scope"] = token_data.get("scope")
    request.session.pop("blog_oauth_state", None)
    request.session.pop("blog_oauth_code_verifier", None)

    return redirect("blog:dashboard")


def dashboard(request):
    access_token = request.session.get("blog_access_token")

    context_profile = None
    error = None
    token_is_valid = False

    if access_token:
        context_profile, error, token_is_valid = _get_context_profile(access_token)
        if not token_is_valid:
            _clear_blog_oauth_session(request)
            access_token = None
        
    return render(
        request,
        "blog/dashboard.html",
        {
            "is_logged_in": bool(access_token and token_is_valid),
            "access_token": access_token,
            "context_profile": context_profile,
            "error": error,
        },
    )


@require_POST
def logout_from_blog(request):
    access_token = request.session.get("blog_access_token")
    refresh_token = request.session.get("blog_refresh_token")

    for token_name, token in (
        ("access_token", access_token),
        ("refresh_token", refresh_token),
    ):
        if not token:
            continue
        # requesting IL-Hub revoke token response
        response = requests.post(
            settings.HUB_REVOKE_TOKEN_URL,
            data={
                "token": token,
                "client_id": settings.BLOG_CLIENT_ID,
                "client_secret": settings.BLOG_CLIENT_SECRET,
            },
            timeout=10,
        )

    _clear_blog_oauth_session(request)

    return redirect("blog:landing")
