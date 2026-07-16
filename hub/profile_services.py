from rest_framework.exceptions import NotFound, PermissionDenied
from .models import LibraryContext, BlogContext
from .serializers import BlogContextSerializer, LibraryContextSerializer


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
            "The requesting client is not configured."
        )

    queryset = client_handler["model"].objects.filter(user=user)

    prefetch_fields = client_handler.get("prefetch", ())
    if prefetch_fields:
        queryset = queryset.prefetch_related(*prefetch_fields)

    profile = queryset.first()

    if profile is None:
        raise NotFound(
            f"No contextual profile exists for client '{client_id}'."
        )

    serializer = client_handler["serializer"](profile)

    return {
        "user_uid": str(user.user_uid),
        "client": client_id,
        "profile": serializer.data,
    }
