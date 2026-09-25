import json
import logging
from datetime import datetime, timezone


class GdprLogJsonFormatter(logging.Formatter):
    """
    Each logging record is converted into one JSON object.
    Notice all values must be inside "gdpr_data" dictionary in order to avoid mix things up with LogRecord fields.
    """

    def format(self, record: logging.LogRecord):
        gdpr_data = getattr(record, "gdpr_data", {})

        payload = {
            "timestamp": self._format_timestamp(record.created),
            "level": record.levelname,
            "logger": record.name,
            "event_type": gdpr_data.get(
                "event_type",
                record.getMessage(),
            ),
            "outcome": gdpr_data.get("outcome"),
            "actor_type": gdpr_data.get("actor_type"),
            "actor_reference": gdpr_data.get("actor_reference"),
            "subject_reference": gdpr_data.get("subject_reference"),
            "metadata": gdpr_data.get("metadata", {}),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    @staticmethod
    def _format_timestamp(created: float):
        """
        Convert a LogRecord creation timestamp.
        """
        timestamp = datetime.fromtimestamp(
            created,
            tz=timezone.utc,
        )

        return timestamp.isoformat(
            timespec="milliseconds",
        ).replace("+00:00", "Z")
