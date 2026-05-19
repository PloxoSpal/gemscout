import asyncio

from dataclasses import dataclass
from fastapi import HTTPException
from typing import Protocol

from src.services.vendors.smsc_api import SMSC

from src.config import settings


class BaseSmsProvider(Protocol):
    async def send_sms(self, number: str, message: str) -> str:
        ...


class SMSCProvider:
    def __init__(self):
        self.client = SMSC()

    async def send_sms(self, phone: str, code: str) -> str:
        if settings.MODE in ['TEST', 'DEV']:
            print(settings.MODE)
            print(f"SMS to {phone}: {code}")
            print(f"Check result: {settings.MODE in ['TEST', 'DEV']}")
            return

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.client.send_sms,
            phone,
            code
        )

        if int(result[1]) < 0:
            raise Exception(f"SMSC ошибка: {result[1]}")

        return result[0]


@dataclass
class SMSService:
    sms_provider: BaseSmsProvider

    async def send_sms(self, phone: str, code: str) -> dict:
        try:
            await self.sms_provider.send_sms(phone, code)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"status": "success"}

smsc_provider = SMSCProvider()
sms_service = SMSService(sms_provider=smsc_provider)