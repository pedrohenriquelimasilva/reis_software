from fastapi import HTTPException
from ..base import BaseHandler
from http import HTTPStatus
from src.models import User
from sqlalchemy import select

class ValidateUserFromTaksHandler(BaseHandler):
    def handle(self, user, session):
        try:
            existing = session.scalar(
                select(User).where(User.email == user.email)
            )

            if not existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email not exists'
                )

            if self._next_handler:
                return self._next_handler.handle(user, session)
            return None
        except Exception as e:
            raise