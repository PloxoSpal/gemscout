from fastapi import APIRouter, Response, Request, HTTPException

from src.config import settings
from src.api.dependencies.db import DBDep
from src.api.dependencies.redis import RedisDep
from src.schemas.users import UserRequest
from src.schemas.auth import ResponseAuthCode
from src.schemas.tokens import TokenVerifyRequest


from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post('/otp/request')
async def request_user(user_data: UserRequest, redis: RedisDep):
    await AuthService().request(user_data, redis)
    return {"status": "success", "message": "code is sent!"}

@router.post('/otp/verify')
async def verify_user_code(
        response: Response,
        user_data: ResponseAuthCode,
        db: DBDep,
        redis: RedisDep
):
    tokens = await AuthService().verify(user_data, db, redis)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=tokens.expires_in,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60*60*24*settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    return {"status": "success"}

@router.post('/otp/refresh')
async def refresh_token(request: Request, response: Response, redis: RedisDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    tokens =  await AuthService().refresh(refresh_token, redis)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=tokens.expires_in,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60*60*24*settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    return {"status": "success"}

@router.post('/otp/logout')
async def logout_user(request: Request, response: Response, redis: RedisDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    await AuthService().logout(refresh_token, redis)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "success"}


@router.get('/me')
async def get_my_profile(request: Request, db: DBDep):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await AuthService().get_me(access_token, db)

@router.post('/verify')
async def verify_user(data: TokenVerifyRequest):
    res = await AuthService().verify_token(data.token)
    return res
