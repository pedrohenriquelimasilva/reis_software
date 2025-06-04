from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import ProgrammingError

from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas import TaskRequestSchema, TaskPutRequestSchema

from src.models import User, Task, TaskStatus
import uuid
class TaskService:
  def __init__(self, validation_handler=None):
    self.validation_handler = validation_handler
    
  def create_task(self, task_data: TaskRequestSchema, session: Session, user: User):
    try:
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(user, session)

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
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(user, session)

      tasks = session.scalars(
          select(Task).where(Task.user_id == user.id)
      ).all()
      
      if not tasks:
        return []

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
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(id,user, session)

      task = session.scalar(
          select(Task).where(Task.id == id)
      )
      
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
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(user, session)

      tasks = session.scalars(
          select(Task).where(
              Task.user_id == user.id,
              Task.status == status
          )
      ).all()

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
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(id, user, session)
      print('cheguei')

      task = session.scalar(
          select(Task).where(Task.id == id)
      )
      print('cheguei')
      
      if not task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Task não encontrada"
            )

      session.delete(task)
      session.commit()
      
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
      # validação de usuario
      if self.validation_handler:
        self.validation_handler.handle(id, user, session)

      task = session.scalar(
        select(Task).where(
            Task.id == id,
            Task.user_id == user.id
        )
      )
      
      if not task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Task não encontrada ou não pertence ao usuário."
            )
      
      for field, value in task_data.model_dump(exclude_unset=True).items():
          setattr(task, field, value)
      
      session.commit()
      session.refresh(task)
      
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