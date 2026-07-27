from enum import Enum


class EventType(str, Enum):
    """
    A strict catalogue of GDPR-relevant event types. This prevents of getting event types out of control.
    """

    LOGIN_SUCCEEDED = "auth.login_succeeded"
    LOGOUT = "auth.logout"

    CONTEXT_PROFILE_ACCESSED = "profile.accessed"
    PROFILE_UPDATED = "profile.updated"

    CLIENT_ACTIVATED = "client.activated"
    CLIENT_DEACTIVATED = "client.deactivated"

    def __str__(self):
        return self.value

    @classmethod
    def values(cls):
        """
        Return all permitted event values.
        """
        return frozenset(event.value for event in cls)

class LogOutcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"


class LogActorType(str, Enum):
    USER = "user"
    ADMINISTRATOR = "administrator"
    OAUTH_CLIENT = "oauth_client"
    SYSTEM = "system"
