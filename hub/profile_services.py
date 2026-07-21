from .models import LibraryContext, BlogContext
from .serializers import BlogContextSerializer, LibraryContextSerializer, ProfileResponseSerializer
from .api_errors import ContextualProfileNotFound, ClientHandlerNotConfigured


PROFILE_HANDLERS = {
    "library": {
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

def get_user_profile(user, client_name, request=None):
    client_handler = PROFILE_HANDLERS.get(client_name)

    if client_handler is None:
        raise ClientHandlerNotConfigured()

    queryset = client_handler["model"].objects.filter(user=user)

    prefetch_fields = client_handler.get("prefetch", ())
    if prefetch_fields:
        queryset = queryset.prefetch_related(*prefetch_fields)

    user_profile = queryset.get()

    if user_profile is None:
        raise ContextualProfileNotFound()

    profile_serializer = client_handler["serializer"](
        user_profile,
        context={"request": request},
        )

    # Formatting and validating data structure  before sending
    response_serializer = ProfileResponseSerializer(
        data = {
            "user_uid": user.user_uid,
            "client": client_name,
            "profile": profile_serializer.data
        }
    )

    response_serializer.is_valid(raise_exception=True)


    return response_serializer.data
