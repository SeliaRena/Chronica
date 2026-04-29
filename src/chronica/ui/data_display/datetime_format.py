from datetime import datetime

_YMD_HMS = "%Y-%m-%d %H:%M:%S"

def ymd_hms(ts_ms_or_datetime: int | datetime) -> str:
    if isinstance(ts_ms_or_datetime, int):
        return datetime.fromtimestamp(ts_ms_or_datetime / 1000).strftime(_YMD_HMS)
    elif isinstance(ts_ms_or_datetime, datetime):
        return ts_ms_or_datetime.strftime(_YMD_HMS)