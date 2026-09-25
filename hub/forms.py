from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import User, LibraryContext, BlogContext
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class HubAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        ),
    )


class LibraryContextForm(forms.ModelForm):
    class Meta:
        model = LibraryContext
        fields = (
            "nickname",
            "interest_topics",
            "email_notifications",
            "photo_path",
        )

        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Library nickname",
                }
            ),
            "interest_topics": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "photo_path": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class BlogContextForm(forms.ModelForm):
    class Meta:
        model = BlogContext
        fields = (
            "nickname",
            "topics",
            "email_notifications",
            "photo_path",
        )

        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Blog nickname",
                }
            ),
            "topics": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "photo_path": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
