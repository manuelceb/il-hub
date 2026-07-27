import logging
from .events import EventType, LogActorType, LogOutcome

audit_logger = logging.getLogger("ilhub.gdpr")

def record_gdpr_log_event(
    *,
    event_type,
    outcome,
    actor_type,
    actor_reference=None,
    subject_reference= None,
    client_reference=None,
    metadata=None,
):
    """
    Validate and write audit log event. 
    It sends records to ilhub.gdpr logger.
    Metadata parameter must be a dict.
    """

    if not isinstance(event_type, EventType):
        raise TypeError(
            "event_type must be an EventType member."
        )

    if outcome not in LogOutcome:
        raise ValueError(
            f"Unsupported log outcome: {outcome!r}"
        )

    if actor_type not in LogActorType:
        raise ValueError(
            f"Unsupported log actor type: {actor_type!r}"
        )

    if metadata is None:
        event_metadata = {}
    elif isinstance(metadata, dict):
        event_metadata = metadata
    else:
        raise TypeError("metadata must be a dict or None.")

    gdpr_data = {
        "event_type": event_type.value,
        "outcome": outcome,
        "actor_type": actor_type,
        "actor_reference": actor_reference,
        "subject_reference": subject_reference,
        "client_reference": client_reference,
        "metadata": event_metadata,
    }

    audit_logger.info(
        event_type.value,
        extra={
            "gdpr_data": gdpr_data,
        },
    )