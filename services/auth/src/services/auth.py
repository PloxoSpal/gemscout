import secrets
from datetime import datetime
from fastapi import HTTPException

from src.schemas.users import UserRequest, UserCreateInternal, UserResponse
from src.schemas.tokens import TokenVerifyResponse
from src.schemas.auth import ResponseAuthCode
from src.api.dependencies.db import DBManager
from src.api.dependencies.redis import RedisManager
from src.services.sms_sender import sms_service
from src.config import settings

from src.utils.jwt_utils import issue_token_pair
from src.utils.jwt_utils import decode_token


class AuthService:
    @staticmethod
    async def request(user_data: UserRequest, redis: RedisManager):
        if not await redis.try_lock_throttle(user_data.phone):
            raise HTTPException(429, "Too many requests")

        if settings.MODE in ["TEST", "DEV"]:
            verify_code = "0000"
        else:
            verify_code = f"{secrets.randbelow(10000):04d}"
            await sms_service.send_sms(phone=user_data.phone, code=verify_code)

        await redis.set_code(user_data.phone, verify_code)


    @staticmethod
    async def verify(auth_data: ResponseAuthCode, db: DBManager, redis: RedisManager):

        current_code = await redis.get_code(auth_data.phone)
        if current_code is None:
            raise HTTPException(400, "Code expired or not requested")

        if current_code != auth_data.code:
            attempts = await redis.incr_attempts(auth_data.phone)
            if attempts >= 5:
                await redis.delete_code(auth_data.phone)
                raise HTTPException(429, "Too many attempts. Request a new code.")
            raise HTTPException(400, "Invalid code, Request a new code.")

        await redis.delete_code(auth_data.phone)
        await redis.reset_attempts(auth_data.phone)

        user = await db.user.get_one_or_none(phone=auth_data.phone)
        if user is None:
            new_user_data = UserCreateInternal(phone=auth_data.phone)
            user = await db.user.add(new_user_data)
            await db.commit()

        return issue_token_pair(user.id)

    @staticmethod
    async def refresh(refresh_token: str | None, redis: RedisManager):
        if not refresh_token:
            raise HTTPException(401, "No refresh token")
        payload = decode_token(refresh_token, expected_type="refresh")
        if await redis.is_blacklisted(payload["jti"]):
            raise HTTPException(400, "Token has been revoked")
        remaining_ttl = int(payload["exp"] - datetime.now().timestamp())
        await redis.blacklist_token(payload["jti"], remaining_ttl)
        return issue_token_pair(int(payload["sub"]))

    @staticmethod
    async def logout(refresh_token: str, redis: RedisManager):
        try:
            payload = decode_token(refresh_token, expected_type="refresh")
            remaining_ttl = int(payload["exp"] - datetime.now().timestamp())
            if remaining_ttl > 0:
                await redis.blacklist_token(payload["jti"], remaining_ttl)
        except HTTPException:
            pass

    @staticmethod
    async def get_me(access_token: str, db: DBManager):
        payload = decode_token(access_token, expected_type="access")
        user = await db.user.get_one_or_none(id=int(payload["sub"]))
        if user is None:
            raise HTTPException(400, "User does not exist")
        return UserResponse.model_validate(user, from_attributes=True)

    @staticmethod
    async def verify_token(token: str) -> TokenVerifyResponse:
        payload = decode_token(token, expected_type="access")
        return TokenVerifyResponse(valid=True, user_id=int(payload["sub"]))








