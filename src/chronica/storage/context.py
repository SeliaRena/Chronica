from dataclasses import dataclass

from src.chronica.storage.sqlite.database import ChronicaDatabase
from src.chronica.storage.sqlite.services import TrackingRecordService

@dataclass(slots=True)
class StorageContext:
    db: ChronicaDatabase
    tracking_records: TrackingRecordService