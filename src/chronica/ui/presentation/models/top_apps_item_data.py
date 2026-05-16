from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

@dataclass(frozen=True, slots=True)
class TopAppsItemData:
    app_name: str
    bar_ratio: float
    share_ratio: float
    duration: str
    icon_path: Path | None = None
    
    EMPTY_ITEM: ClassVar[TopAppsItemData]

TopAppsItemData.EMPTY_ITEM = TopAppsItemData(
    app_name="N/A",
    bar_ratio=0.0,
    share_ratio=0.0,
    duration="N/A",
    icon_path=None
)