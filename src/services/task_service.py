from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import ProgrammingError

from sqlalchemy.orm import Session
from src.schemas import TaskRequestSchema

from src.models import User, Task, TaskStatus


class TaskService:
  def __init__(self, validation_handler=None):
    self.validation_handler = validation_handler
    
  def create_task(self, task_data: TaskRequestSchema, session: Session, user: User):
    try:
      # validação de usuario
      print('antes do handler')
      if self.validation_handler:
        self.validation_handler.handle(user, session)
      print('depois do handler')

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