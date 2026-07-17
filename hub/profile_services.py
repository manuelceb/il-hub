from rest_framework.exceptions import NotFound, PermissionDenied
from .models import LibraryContext, BlogContext
from .serializers import BlogContextSerializer, LibraryContextSerializer, ProfileResponseSerializer


CLIENT_REGISTRY = {
    "M3NwNfUD7ZolzA5mb81InHAfzbuZjZrsluFtgjBj": {
        "client_name": "library",
        "model": LibraryContext,
        "serializer": LibraryContextSerializer,
        "prefetch": ("interest_topics",),
    },
    "blog": {
        "model": BlogContext,
        "serializer": BlogContextSerializer,
        "prefetch": ("topics",),
    },
}

def get_user_profile(user, client_id):
    client_handler = CLIENT_REGISTRY.get(client_id)

    if client_handler is None:
        raise PermissionDenied(
            "The requesting client is not identified."
        )

    queryset = client_handler["model"].objects.filter(user=user)

    prefetch_fields = client_handler.get("prefetch", ())
    if prefetch_fields:
        queryset = queryset.prefetch_related(*prefetch_fields)

    user_profile = queryset.first()

    if user_profile is None:
        raise NotFound(
            f"No profile exists for client: {client_id} and user {user}'."
        )

    profile_serializer = client_handler["serializer"](user_profile)

    # Formatting and validating data structure  before sending
    response_serializer = ProfileResponseSerializer(
        data = {
            "user_uid": user.user_uid,
            "client": client_id,
            "profile": profile_serializer.data
        }
    )

    response_serializer.is_valid(raise_exception=True)


    return response_serializer.data
