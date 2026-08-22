from django.views.generic import TemplateView, UpdateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from .profile_services import get_user_profile
from oauth2_provider.contrib.rest_framework import OAuth2Authentication,TokenHasScope
from .models import ClientRegistry, LibraryContext, BlogContext
from .api_errors import ClientInactive, TokenClientError, ClientNotRegistered
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LibraryContextForm, BlogContextForm, HubAuthenticationForm
from .logging_services.events import EventType
from .logging_services.logging_service import record_gdpr_log_event   


class UserDataDashboardView(LoginRequiredMixin, TemplateView,):
    template_name = "hub/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_name = self.request.user.email
        context["display_name"] = display_name
        return context


class HubLoginView(LoginView):
    template_name = "hub/login.html"
    authentication_form = HubAuthenticationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_name = None
        if self.request.user and self.request.user.is_authenticated:
            display_name = self.request.user.email
            
        context["display_name"] = display_name
        return context

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
            event_type=EventType.PROFILE_ACCESSED,
            outcome="success",
            actor_type= "oauth_client",
            actor_reference=client_name,
            subject_reference=user_reference,
        )

        return Response(data)

class LibraryProfileView(LoginRequiredMixin, TemplateView):

    template_name = "hub/partials/library_profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["profile"] = LibraryContext.objects.get(user=self.request.user)
        return context
    
class BlogProfileView(LoginRequiredMixin, TemplateView,):
    template_name = "hub/partials/blog_profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["profile"] = BlogContext.objects.get(user=self.request.user)
        return context

class HubProfileView(LoginRequiredMixin, TemplateView):
    template_name = "hub/partials/hub_profile.html"


class LibraryProfileEditView(LoginRequiredMixin, UpdateView):
    model = LibraryContext
    form_class = LibraryContextForm
    template_name = "hub/partials/library_profile_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            LibraryContext,
            user=self.request.user,
        )

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        request = self.request
        user_uid = getattr(user, "user_uid", None)
        user_uid = str(user_uid)
        record_gdpr_log_event(
                    event_type=EventType.PROFILE_UPDATED,
                    outcome="success",
                    actor_type= "user",
                    actor_reference=user_uid,
                    subject_reference=user_uid,
                    metadata={"device":request.META.get('HTTP_USER_AGENT', ''),
                                "client profile updated": "library",
                              }
        )

        return render(
            self.request,
            "hub/partials/library_profile.html",
            {"profile": self.object},
        )

class BlogProfileEditView(LoginRequiredMixin, UpdateView):
    model = BlogContext
    form_class = BlogContextForm
    template_name = "hub/partials/blog_profile_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            BlogContext,
            user=self.request.user,
        )

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        request = self.request
        user_uid = getattr(user, "user_uid", None)
        user_uid = str(user_uid)
        record_gdpr_log_event(
            event_type=EventType.PROFILE_UPDATED,
            outcome="success",
            actor_type= "user",
            actor_reference=user_uid,
            subject_reference=user_uid,
            metadata={"device":request.META.get('HTTP_USER_AGENT', ''),
                       "client profile updated": "library",
                      }
        )

        return render(
            self.request,
            "hub/partials/blog_profile.html",
            {"profile": self.object},
        )