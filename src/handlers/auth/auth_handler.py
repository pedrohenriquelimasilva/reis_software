from src.models import User
from src.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from http import HTTPStatus

class AuthHandler:
    def __init__(self, session: Session):
        self.session = session

    def authenticate_user(self, email: str, password: str):
        user = self.session.scalar(
            select(User).where(User.email == email)
        )

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email incorreto',
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Senha incorreta',
            )

        return user

    def create_token(self, user: User):
        return create_access_token(data={'sub': user.email, 'user_id': str(user.id)})
  
