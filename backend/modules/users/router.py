from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.auth import get_current_user
from backend.core.db import get_db
from backend.modules.users.schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from backend.modules.users.service import (
    EmailAlreadyRegistered,
    HandleAlreadyTaken,
    InvalidCredentials,
    UserNotFound,
    UserService,
)

router = APIRouter(tags=["Users"])


@router.post(
    "/api/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        user = await service.register(data)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    except HandleAlreadyTaken:
        raise HTTPException(status_code=400, detail="Хэндл уже занят")
    return user


@router.post("/api/auth/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        token = await service.authenticate(data.email, data.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    return TokenResponse(access_token=token)


@router.get("/api/users/me", response_model=UserResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    service = UserService(db)
    try:
        user = await service.get_profile(user_id)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
