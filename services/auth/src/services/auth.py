import random
from fastapi import HTTPException

from src.schemas.users import UserRequest
from src.schemas.auth import ResponseAuthCode
from src.api.dependencies.db import DBManager
from src.api.dependencies.redis import RedisManager

from src.services.sms_sender import sms_service

from src.config import settings

class AuthService:
    async def register(self, user_data: UserRequest, db: DBManager, redis: RedisManager):
        existing = await db.user.get_one_or_none(phone=user_data.phone)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        if settings.MODE in ['TEST', 'DEV']:
            verify_code = 0000
        else:
            verify_code = random.randint(1000, 9999)
        await redis.set_code(user_data.phone, verify_code)
        await sms_service.send_sms(phone=user_data.phone, code=verify_code)
        return {"status": "Сообщение отправлено!", "number": user_data.phone}

    async def verify_sms_code(self, auth_data: ResponseAuthCode, db: DBManager, redis: RedisManager):
        current_code = await redis.get_code(auth_data.phone)
        if int(current_code) == int(auth_data.code):
            return {"status": "Успешная регистрация!"}
        else:
            return {"status": "Неверный код!"}




