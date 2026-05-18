from fastapi import APIRouter

from src.schemas.users import UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    ...