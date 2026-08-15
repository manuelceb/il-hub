from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
            "interest_topics": forms.CheckboxSelectMultiple(),
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
            "topics": forms.CheckboxSelectMultiple(),
        }

