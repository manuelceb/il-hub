from rest_framework import serializers

from .models import BlogContext, LibraryContext


class LibraryContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryContext
        fields = (
            "nickname",
            "created_at",
            "modified_at",
            "email_notifications",
            "photo_path",
            "interest_topics"
        )


class BlogContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContext
        fields = (
            "nickname",
            "created_at",
            "modified_at",
            "email_notifications",
            "photo_path",
            "topics"
        )