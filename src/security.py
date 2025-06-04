from fastapi import Depends, HTTPException
from http import HTTPStatus

from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.settings import Settings
from src.models import User
from src.database import get_session

from sqlalchemy import select
from sqlalchemy.orm import Session


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ----- PASSWORD --------
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
  
# ----- TOKEN --------

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=float(Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username = payload.get("sub")
        exp = payload.get("exp")
        user_id = payload.get("user_id")

        if not username or not user_id:
            raise credentials_exception

        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise credentials_exception

        # Verifica se não expirou (em geral o jose já faz isso, mas é só um check extra)
        if exp and datetime.fromtimestamp(exp, tz=ZoneInfo("UTC")) < datetime.now(
            tz=ZoneInfo("UTC")
        ):
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception