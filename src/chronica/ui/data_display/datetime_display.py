from datetime import datetime

_YMD_HMS = "%Y-%m-%d %H:%M:%S"

def ymd_hms(dt: datetime) -> str:
    """
    This function assumes the datetime already contains timezone information \n
    Only use for data display or in UI (abstractions eq or higher than display models)
    """
    return dt.strftime(_YMD_HMS)