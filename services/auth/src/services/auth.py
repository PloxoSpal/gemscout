from fastapi import HTTPException

from src.schemas.users import UserRequest
from src.schemas.auth import ResponseAuthCode
from src.api.dependencies.db import DBManager
from src.api.dependencies.redis import RedisManager

class AuthService:

    async def register(self, user_data: UserRequest, db: DBManager, redis: RedisManager):
        existing = await db.user.get_one_or_none(phone=user_data.phone)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        verify_code = 1235

        await redis.set_code(user_data.phone, value=verify_code)

        #тут мы как будто бы отправили пользователю этот код на телефон.

    async def verify_sms_code(self, auth_data: ResponseAuthCode, db: DBManager, redis: RedisManager):
        current_code = await redis.get_code(auth_data.phone)
        if int(current_code) == int(auth_data.code):
            return {"status": "Успешная регистрация!"}
        else:
            return {"status": "Неверный код!"}




