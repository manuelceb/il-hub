from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    User,
    LibraryContext,
    LibraryInterestTopics,
    BlogContext,
    BlogTopics,
    ClientRegistry,
)


class LibraryContextInline(admin.StackedInline):
    model = LibraryContext
    extra = 0
    max_num = 1

    fields = (
        "nickname",
        "interest_topics",
        "email_notifications",
        "photo_path",
        "created_at",
        "modified_at",
    )

    readonly_fields = (
        "created_at",
        "modified_at",
    )

    filter_horizontal = (
        "interest_topics",
    )


class BlogContextInline(admin.StackedInline):
    model = BlogContext
    extra = 0
    max_num = 1

    fields = (
        "nickname",
        "topics",
        "email_notifications",
        "photo_path",
        "created_at",
        "modified_at",
        "photo_modified_at",
    )

    readonly_fields = (
        "created_at",
        "modified_at",
        "photo_modified_at",
    )

    filter_horizontal = (
        "topics",
    )


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)

    inlines = (
        LibraryContextInline,
        BlogContextInline,
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(LibraryInterestTopics)
class LibraryInterestTopicsAdmin(admin.ModelAdmin):
    list_display = ("topics",)
    search_fields = ("topics",)


@admin.register(BlogTopics)
class BlogTopicsAdmin(admin.ModelAdmin):
    list_display = ("topics",)
    search_fields = ("topics",)


@admin.register(ClientRegistry)
class ClientRegistryAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "is_active",
    )