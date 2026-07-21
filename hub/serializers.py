from rest_framework import serializers
from .models import BlogContext, LibraryContext

class ProfileResponseSerializer(serializers.Serializer):
    """ Class that acts as a wrapper validating and formatting the final API response structure. """
    user_uid = serializers.UUIDField()
    client = serializers.CharField(max_length = 25)
    profile = serializers.DictField()

class LibraryContextSerializer(serializers.ModelSerializer):
    interest_topics = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = "topics"
    )
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
    topics = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = "topics"
    )
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


class ApiErrorSerializer(serializers.Serializer):
    """
    Describes the standard error response returned by the API, intended for documentation
    The exception handler constructs the response dictionary directly.
    """

    code = serializers.CharField(
        help_text="Machine-readable error identifier."
    )
    message = serializers.CharField(
        help_text="Human-readable error description."
    )