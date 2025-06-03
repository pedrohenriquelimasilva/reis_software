from fastapi import APIRouter, Depends, HTTPException, Request, Response
from http import HTTPStatus

from src.models import Task, User
from src.schemas import UserPublicSchema, UserRequestSchema
from src.database import get_session
from src.handlers.user.user_handler import EmailDuplicationHandler
from src.services.user_service import UserService

from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

Session_db = Annotated[Session, Depends(get_session)]

@router.post(
  '/register', 
  status_code=HTTPStatus.CREATED,
  response_model=UserPublicSchema,
  summary='Criar usuário na base de dados.',
  description='Rota destinada para criação de usuários na base de dados.'
)
def creat_user(session: Session_db, data_of_new_user: UserRequestSchema):
  email_handler = EmailDuplicationHandler()
  
  service = UserService(validation_handler=email_handler)
  
  return service.create_user(session=session, user_data=data_of_new_user)