from pydantic import BaseModel, EmailStr
from typing import Optional
from __future__ import annotations


class UserCreate(BaseModel):
    nombre: str                     # obligatorio
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
