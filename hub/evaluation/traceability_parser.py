import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / "logs" / "gdpr_logs.jsonl"

def parse_timestamp(timestamp):
    """
    It converts the UTC format used by the logger system inot a python datetime format.
    """
    return datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

def load_json_file():
    records = []
    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records

def filter_by_user_and_date(records, subject_reference, start_timestamp, finish_timestamp,):

    """
    It retrieves all audit events involving the specified Resource Owner
        during the given time interval.
    """
    start = parse_timestamp(start_timestamp)
    finish = parse_timestamp(finish_timestamp)
    filtered_records = []

    for record in records:
        timestamp = parse_timestamp(record["timestamp"])

        user_match = (record.get("subject_reference") == subject_reference,)
        date_match = start <= timestamp <= finish
        if user_match and date_match:
            filtered_records.append(record)

    return filtered_records

def trace_user_activity(start_timestamp, finish_timestamp, subject_reference):
    records = load_json_file()

    return filter_by_user_and_date(
        records=records,
        subject_reference=subject_reference,
        start_timestamp=start_timestamp,
        finish_timestamp=finish_timestamp
    )

if __name__ == "__main__":

    SUBJECT_REFERENCE = "166c3dd1-abc7-479a-8295-6be9515f3516"

    START_TIMESTAMP = "2026-08-22T21:24:00.255Z"
    FINISH_TIMESTAMP = "2026-08-22T22:13:00.000Z"

    activity = trace_user_activity(
        subject_reference=SUBJECT_REFERENCE ,
        start_timestamp=START_TIMESTAMP,
        finish_timestamp=FINISH_TIMESTAMP,
    )

    for event in activity:
        if event["event_type"] == "profile.accessed":
            
            print(
                event["timestamp"],
                "-",
                event["event_type"],
                "-",
                event["actor_reference"]
            )
        else:
            print(
                event["timestamp"],
                "-",
                event["event_type"],
            )