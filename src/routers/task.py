from fastapi import APIRouter, Depends, Path, Query
from http import HTTPStatus

from src.schemas import TaskPublicSchema, TaskRequestSchema, TasksPublicShema, TaskDeletePublicSchema, TaskPutRequestSchema
from src.database import get_session
from src.handlers.tasks.tasks_handler import ValidateIDTaksHandler
from src.services.task_service import TaskService
from src.models import User, TaskStatus
from src.security import get_current_user
from typing import Optional
from sqlalchemy.orm import Session
from typing import Annotated
import uuid
from datetime import datetime

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
  summary='Criar tarefa na base de dados.',
  description='Rota destinada para criação de tarefa na base de dados.'
)
def creat_task(session: Session_db, user: CurrentUser, data_task: TaskRequestSchema):
  service = TaskService()
  
  return service.create_task(session=session, task_data=data_task, user=user)



@router.get(
  '', 
  status_code=HTTPStatus.OK,
  response_model=Optional[TasksPublicShema],
  summary='Buscar tarefas no banco de dados.',
  description='Rota destinada para busca de todas as tarefas da base de dados.'
)
def get_all_tasks(session: Session_db, user: CurrentUser):
  service = TaskService()

  tasks = service.get_all_task(session=session, user=user)

  return {"tasks": tasks}



@router.get(
  '/{id}', 
  status_code=HTTPStatus.OK,
  response_model=TaskPublicSchema,
  summary='Buscar tarefa no banco de dados.',
  description='Rota destinada para busca de uma tarefa especifica na base de dados pelo ID.'
)
def get_task_by_id(
  session: Session_db, 
  user: CurrentUser,
  id: uuid.UUID = Path(..., description="ID da task a ser buscada"),
):
  task_handler = ValidateIDTaksHandler()
  
  service = TaskService(validation_handler=task_handler)

  return service.get_task(session=session, user=user, id=id)


@router.get(
  '/', 
  status_code=HTTPStatus.OK,
  response_model=Optional[TasksPublicShema],
  summary='Filtrar tarefa no banco de dados.',
  description='Rota destinada para filtrar as tarefa na base de pelo dados status.'
)
def filter_taks_by_status(
  session: Session_db, 
  user: CurrentUser,
  status: TaskStatus = Query(..., description="Status da task (completed ou pending)"),
):

  service = TaskService()
  
  tasks = service.get_task_by_status(session=session, user=user, status=status.value)
  
  return {'tasks': tasks}



@router.delete(
  '/{id}', 
  status_code=HTTPStatus.OK,
  response_model=TaskDeletePublicSchema,
  summary='Deletar tarefa no banco de dados.',
  description='Rota destinada para deletar uma tarefa especifica na base de dados pelo ID.'
)
def delete_task_by_id(
  session: Session_db, 
  user: CurrentUser,
  id: uuid.UUID = Path(..., description="ID da task a ser deletada"),
):
  task_handler = ValidateIDTaksHandler()

  service = TaskService(validation_handler=task_handler)

  return service.delete_task_by_id(session=session, user=user, id=id)



@router.put(
  '/{id}', 
  status_code=HTTPStatus.OK,
  response_model=TaskPublicSchema,
  summary='Modificar tarefa no banco de dados.',
  description='Rota destinada para modicar uma tarefa especifica na base de dados pelo ID.'
)
def put_task_by_id(
  session: Session_db, 
  user: CurrentUser,
  task_data: TaskPutRequestSchema,
  id: uuid.UUID = Path(..., description="ID da task a ser modificada"),
):
  task_handler = ValidateIDTaksHandler()

  service = TaskService(validation_handler=task_handler)

  return service.put_task_by_id(session=session, user=user, id=id, task_data=task_data)
