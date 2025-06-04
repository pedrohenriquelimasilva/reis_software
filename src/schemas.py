from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from src.models import TaskStatus
import uuid

class UserPublicSchema(BaseModel):
    name: str
    createdAt: datetime
    
class UserRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenPublicSchema(BaseModel):
    access_token: str
    token_type: str

class TokenRequestSchema(BaseModel):
    email: EmailStr
    password: str
class TaskPublicSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None

class TaskRequestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None