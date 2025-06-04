from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus

from src.models import Task, User
from src.schemas import UserPublicSchema, UserRequestSchema, TokenPublicSchema
from src.database import get_session
from src.handlers.user.user_handler import EmailDuplicationHandler
from src.services.user_service import UserService
from src.services.auth_service import AuthService

from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

Session_db = Annotated[Session, Depends(get_session)]
oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

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


@router.post(
  '/login', 
  status_code=HTTPStatus.OK,
  response_model=TokenPublicSchema,
  summary='Login com e-mail e senha',
  description='Autentica o usuário usando email e senha e retorna um access_token. O Token é retornado no corpo da resposta.'
)
def login(session: Session_db, form_data: oauth2Form):
  try: 
    auth_service = AuthService(session)
    
    access_token = auth_service.login(
            form_data.username, form_data.password
    )
    
    return {
      'access_token': access_token,
      'token_type': 'Bearer'
    }
  except HTTPException as e:
      raise e
  except Exception as e:
      raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))