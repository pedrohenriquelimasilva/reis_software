from pydantic import BaseModel, EmailStr
from datetime import datetime

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