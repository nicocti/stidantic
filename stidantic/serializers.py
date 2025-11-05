from datetime import datetime, timezone


def ser_datetime(value: datetime) -> str:
    """
    The timestamp property MUST be a valid RFC 3339-formatted timestamp [RFC3339] using the format
    YYYY-MM-DDTHH:mm:ss[.s+]Z where the "s+" represents 1 or more sub-second values.
    The brackets denote that sub-second precision is optional, and that if no digits are provided,
    the decimal place MUST NOT be present.
    The timestamp MUST be represented in the UTC timezone and MUST use the "Z" designation to indicate this.
    NOTE: when using precisions greater than nanoseconds there may be implications for interoperability as they may be
    truncated when stored as a UNIX timestamp or floating point number due to the precision of those formats.
    """
    if value.microsecond == 0:
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
