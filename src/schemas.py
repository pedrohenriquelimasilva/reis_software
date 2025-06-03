from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserPublicSchema(BaseModel):
    name: str
    createdAt: datetime
    
class UserRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str