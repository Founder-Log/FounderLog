from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.core.db import get_db



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")   #заранее вписал путь к login

#сделаю поиск юзера в бд когда будут таблицы
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Failed to validate the token")
        
    except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="The token is invalid or has expired")