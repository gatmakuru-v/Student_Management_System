from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class Student(BaseModel):
    name: str
    age: int
    course: str
    email: EmailStr
    phone: str
    address: str
    enrollment_date: Optional[datetime] = datetime.utcnow()
    is_active: bool = True

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[datetime] = None
    is_active: Optional[bool] = None
