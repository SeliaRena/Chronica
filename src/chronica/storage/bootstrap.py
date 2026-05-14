from src.chronica.storage.sqlite.database import ChronicaDatabase
from src.chronica.storage.sqlite.schema import initialize_schema
from src.chronica.storage.sqlite.repositories import TrackingRecordRepository
from src.chronica.storage.sqlite.services import TrackingRecordService
from src.chronica.storage.context import StorageContext
from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.common.paths import DB_PATH

def build_sqlite_storage_context(ts_ctx_provider: TimestampContextProvider) -> StorageContext:
    db = ChronicaDatabase(DB_PATH)
    initialize_schema(db)
    
    tracking_record_repo = TrackingRecordRepository(db)
    
    return StorageContext(
        db=db, 
        tracking_records=TrackingRecordService(
            repo=tracking_record_repo,
            ts_ctx_provider=ts_ctx_provider
        )
    )