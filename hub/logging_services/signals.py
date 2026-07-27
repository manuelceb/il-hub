from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .events import EventType
from .logging_service import record_gdpr_log_event

"""
Using Django signals emmited during login process.
Using user_uid to trace each request and store as log event according to defined in events.py
"""

@receiver(user_logged_in, dispatch_uid="hub.logging_services.login_succeeded",)
def successful_login(user, request, **kwargs):
    """
    Record a successful Django authentication event.
    """
    user_uid = getattr(user, "user_uid", None)
    user_uid = str(user_uid)

    record_gdpr_log_event(
        event_type=EventType.LOGIN_SUCCEEDED,
        outcome="success",
        actor_type="user",
        actor_reference=user_uid,
        subject_reference=user_uid,
        metadata={"device":request.META.get('HTTP_USER_AGENT', ''),}
    )