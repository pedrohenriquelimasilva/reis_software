from fastapi import HTTPException
from ..base import BaseHandler
from http import HTTPStatus
from src.models import User
from sqlalchemy import select

class EmailDuplicationHandler(BaseHandler):
    def handle(self, request, session):
        try:
            existing = session.scalar(
                select(User).where(User.email == request.email)
            )

            if existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists'
                )

            if self._next_handler:
                return self._next_handler.handle(request, session)
            return None
        except Exception as e:
            raise