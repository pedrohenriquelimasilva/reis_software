from datetime import date, datetime
from enum import Enum
from sqlalchemy import DateTime, String, UUID, ForeignKey
from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, registry
import uuid

table_registry = registry()

class TaskStatus(str, Enum):
  PENDING = 'pending'
  COMPLETED = 'completed'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(default=datetime.now())
    
    
@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = "task"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    due_date: Mapped[datetime] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SqlAlchemyEnum(TaskStatus, name='taskstatus'), nullable=False, default=TaskStatus.PENDING)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime ,default=datetime.now(), onupdate=datetime.now())