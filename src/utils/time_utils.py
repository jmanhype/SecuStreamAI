from datetime import datetime

def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)

def datetime_to_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())