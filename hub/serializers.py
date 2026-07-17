from rest_framework import serializers
from .models import BlogContext, LibraryContext

class ProfileResponseSerializer(serializers.Serializer):
    """ Class that acts as a wrapper validating and formatting the final API response structure. """
    user_uid = serializers.UUIDField()
    client = serializers.CharField(max_lenght = 100)
    profile = serializers.DictField()

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