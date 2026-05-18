from fastapi import APIRouter
from fastapi import HTTPException

from src.api.dependencies.db import DBDep
from src.api.dependencies.redis import RedisDep
from src.schemas.users import UserRequest
from src.schemas.auth import ResponseAuthCode

from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post('/register')
async def register_user(user_data: UserRequest, db: DBDep, redis: RedisDep):
    await AuthService().register(user_data, db, redis)

@router.post('/verify')
async def register_user(user_data: ResponseAuthCode, db: DBDep, redis: RedisDep):
    res = await AuthService().verify_sms_code(user_data, db, redis)
    return {"status": res}

