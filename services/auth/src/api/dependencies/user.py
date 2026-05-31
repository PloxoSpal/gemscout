from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from src.api.dependencies.db import DBDep
from src.config import settings

from src.models.users import UserOrm

bearer = HTTPBearer()

async def get_current_user(
        creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        db: DBDep,
) -> UserOrm:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(creds.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    if payload.get("type") != 'access':
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await db.user.get_one_or_none(id=user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(user = Annotated[UserOrm,Depends(get_current_user)]):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

CurrentUser = Annotated[UserOrm, Depends(get_current_active_user)]