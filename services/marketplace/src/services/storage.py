import os
from uuid import uuid4
from typing import Protocol
from dataclasses import dataclass
from fastapi import UploadFile

from src.config import settings

class StorageProvider(Protocol):
    async def upload(self, file: UploadFile, path: str):
        ...

    async def delete(self, file_url: str):
        ...

class S3Provider:
    def __init__(self, client) -> None:
        self.client =client

    async def upload(self, file: UploadFile, path: str):
        content = await file.read()
        f_ext = os.path.splitext(file.filename)[1] if file.filename else ""
        key = f'{path}/{uuid4()}{f_ext}'

        await self.client.put_object(
            Body=content,
            Bucket=settings.BUCKET_NAME,
            Key=key
        )
        return f'https://{settings.ENDPOINT_URL}/{key}'

    async def delete(self, file_url: str):

        key = file_url.replace(f'https://{settings.ENDPOINT_URL}/', "")
        await self.client.delete_object(
            Bucket=settings.BUCKET_NAME,
            Key=key
        )

@dataclass
class StorageService:
    storage_provider: StorageProvider

    async def upload_profile_image(self, file: UploadFile):
        return await self.storage_provider.upload(file, 'profile')

    async def upload_passport_image(self, file: UploadFile):
        return await self.storage_provider.upload(file, 'passport')

    async def delete_image(self, file_url: str):
        return await self.storage_provider.delete(file_url)
