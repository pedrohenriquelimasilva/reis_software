from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import ProgrammingError

from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas import TaskRequestSchema, TaskPutRequestSchema

from src.models import User, Task, TaskStatus
import uuid
from src.utils.logger import log_time

class TaskService:
  def __init__(self, validation_handler=None):
    self.validation_handler = validation_handler
    
  def create_task(self, task_data: TaskRequestSchema, session: Session, user: User):
    try:
      log_time('Validation user')
      if self.validation_handler:
        self.validation_handler.handle(user, session)
      
      log_time('Config info task')
      task = Task(
        title=task_data.title,
        description=task_data.description,
        status=TaskStatus.PENDING,
        due_date=task_data.due_date,
        user_id=str(user.id)
      )
      
      session.add(task)
      session.commit()
      session.refresh(task)
      log_time('create task in db')
      
      return task
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao criar Task"
        )
  
  def get_all_task(self, session: Session, user: User):
    try:
      log_time('Validation user')
      if self.validation_handler:
        self.validation_handler.handle(user, session)
      
      log_time('Search task in db by id user')
      
      tasks = session.scalars(
          select(Task).where(
            Task.user_id == user.id,
            Task.is_inactive == False
          )
      ).all()
      
      if not tasks:
        return []
      log_time('Return all task from user')

      return tasks
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao acessar as Task"
        )
  
  def get_task(self, id: uuid.UUID, session: Session, user: User):
    try:
      log_time('Validation user')
      if self.validation_handler:
        self.validation_handler.handle(id,user, session)
      
      log_time('Search task in db by id task')

      task = session.scalar(
          select(Task).where(
            Task.id == id,
            Task.is_inactive == False
          )
      )
      log_time('Return task by id')
      
      return task
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao acessar Task"
        )
  
  def get_task_by_status(self, status: str, session: Session, user: User):
    try:
      log_time('Validation user')
      if self.validation_handler:
        self.validation_handler.handle(user, session)

      log_time('Search all task in db by status task')
      
      tasks = session.scalars(
          select(Task).where(
              Task.user_id == user.id,
              Task.status == status,
              Task.is_inactive == False
          )
      ).all()
      
      log_time('Return all task by status from user')

      return tasks
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao acessar Task"
        )
        
        
  def delete_task_by_id(self, id: uuid.UUID, session: Session, user: User):
    try:
      log_time('Validation user')
      if self.validation_handler:
        self.validation_handler.handle(id, user, session)

      log_time('Search task')

      task = session.scalar(
          select(Task).where(Task.id == id)
      )
      
      if not task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Task não encontrada"
            )
      task.is_inactive = True

      session.commit()
      session.refresh(task)
      log_time('Inactive task by ID')
      
      return {"detail": "Task deletada com sucesso"}
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao acessar Task"
        )
    
  
  def put_task_by_id(self, id: uuid.UUID, task_data: TaskPutRequestSchema, session: Session, user: User):
    try:
      log_time('Validation user')

      if self.validation_handler:
        self.validation_handler.handle(id, user, session)

      log_time('Search task')

      task = session.scalar(
        select(Task).where(
            Task.id == id,
            Task.user_id == user.id,
            Task.is_inactive == False
        )
      )
      
      if not task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Task não encontrada ou não pertence ao usuário."
            )
      
      log_time('put datas by task')
      
      for field, value in task_data.model_dump(exclude_unset=True).items():
          setattr(task, field, value)
      
      session.commit()
      session.refresh(task)
      
      log_time('Commit task in db')
      
      return task
    except ProgrammingError as e:
      raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao acessar Task"
        )