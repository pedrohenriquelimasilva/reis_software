from fastapi import APIRouter, Depends
from http import HTTPStatus

from src.schemas import TaskPublicSchema, TaskRequestSchema
from src.database import get_session
from src.handlers.tasks.tasks_handler import ValidateUserFromTaksHandler
from src.services.task_service import TaskService
from src.models import User
from src.security import get_current_user

from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)

Session_db = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
@router.post(
  '', 
  status_code=HTTPStatus.CREATED,
  response_model=TaskPublicSchema,
  summary='Criar task na base de dados.',
  description='Rota destinada para criação de task na base de dados.'
)
def creat_task(session: Session_db, user: CurrentUser, data_task: TaskRequestSchema):
  user_validate = ValidateUserFromTaksHandler()
  
  service = TaskService(validation_handler=user_validate)
  
  return service.create_task(session=session, task_data=data_task, user=user)