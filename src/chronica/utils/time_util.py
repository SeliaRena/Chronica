import time

def get_current_unix_timestamp_ms() -> int:
    """A convenient function to get the current Unix timestamp in milliseconds. \n

    Returns:
        int: The current Unix timestamp in milliseconds.
    """
    
    return int(time.time_ns() // 1_000_000)