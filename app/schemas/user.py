from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    is_active: bool
    is_admin: bool
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)
    


class Token(BaseModel):
    access_token: str
    token_type: str