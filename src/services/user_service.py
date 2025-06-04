from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import ProgrammingError, IntegrityError

from sqlalchemy.orm import Session
from src.schemas import UserRequestSchema

from src.models import User

from src.security import get_password_hash

class UserService:
  def __init__(self, validation_handler=None):
    self.validation_handler = validation_handler
    
  def create_user(self, user_data: UserRequestSchema, session: Session):
    try:
      # validação de email
      if self.validation_handler:
        self.validation_handler.handle(user_data, session)
      
      user = User(
        name=user_data.name,
        email=user_data.email,
        password=get_password_hash(user_data.password)
      )
      
      session.add(user)
      session.commit()
      session.refresh(user)
      
      return user
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Usuário com email já cadastrado."
        )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao criar usuário."
        )