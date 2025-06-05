from fastapi import HTTPException
from src.handlers.base import BaseHandler
from http import HTTPStatus
from src.models import Task
from sqlalchemy import select

class ValidateIDTaksHandler(BaseHandler):
    def handle(self, id, user, session):
        try:
            existing = session.scalar(
                select(Task).where(
                    Task.id == id,
                    Task.user_id == user.id,
                    Task.is_inactive == False
                )
            )
            
            if not existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Task not exists'
                )

            if self._next_handler:
                return self._next_handler.handle(user, session)
            
            return None
        except Exception as e:
            raise