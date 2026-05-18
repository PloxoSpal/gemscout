from typing import Annotated

from fastapi import Depends

from src.storage import s3_provider
from src.services.storage import StorageService

def get_storage_service():
    return StorageService(storage_provider=s3_provider)

StorageDep = Annotated[StorageService, Depends(get_storage_service)]