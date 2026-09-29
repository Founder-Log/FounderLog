from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # заранее вписал путь к login


def create_access_token(user_id: int, is_admin: bool = False) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "is_admin": is_admin, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Failed to validate the token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="The token is invalid or has expired")

    return int(user_id)


_optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", auto_error=False
)

async def get_current_admin(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        is_admin = payload.get("is_admin", False)

        if user_id is None or not is_admin:
            raise HTTPException(status_code=403, detail="Требуются права администратора")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="The token is invalid or has expired")

    return int(user_id)


async def get_current_user_optional(
    token: str | None = Depends(_optional_oauth2_scheme),
) -> int | None:
    if token is None:
        return None

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            return None
    except jwt.PyJWTError:
        return None

    return int(user_id)
