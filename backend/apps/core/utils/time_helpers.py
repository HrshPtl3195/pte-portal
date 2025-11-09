from datetime import datetime, timezone




def now_utc():
    return datetime.now(timezone.utc)




def to_unix(dt: datetime) -> int:
    return int(dt.timestamp())




def from_unix(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)