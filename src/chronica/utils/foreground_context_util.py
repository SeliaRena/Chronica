from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from src.chronica.common.errors import ForegroundContextAquisitionError
from src.chronica.utils.time_util import get_current_unix_timestamp_ms
import psutil
import win32gui
import win32process

@dataclass(frozen=True)
class ForegroundContext:
    hwnd: int
    pid: int
    window_title: str
    exe: str
    exe_name: str
    acquired_ts_ms: int = field(default_factory=get_current_unix_timestamp_ms)
    
def same_window(ctx1: ForegroundContext, ctx2: ForegroundContext) -> bool:
    """
    ### Checks if two foreground contexts belong to the same window. \n
    Strictly equivalent to checking if the two contexts have the same executable name and window title.

    Args:
        ctx1 (ForegroundContext): no desc
        ctx2 (ForegroundContext): no desc

    Returns:
        bool: True if both contexts belong to the same window of the same application, False otherwise
    """
    return ctx1.exe_name == ctx2.exe_name and ctx1.window_title == ctx2.window_title
    
def get_foreground_context() -> ForegroundContext:
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        title = win32gui.GetWindowText(hwnd)
        exe = process.exe()
        exe_name = Path(exe).name
        
        return ForegroundContext(hwnd=hwnd, pid=pid, window_title=title, exe=exe, exe_name=exe_name)
    except Exception as e:
        raise ForegroundContextAquisitionError(f"Failed to acquire current foreground context: {e}") from e