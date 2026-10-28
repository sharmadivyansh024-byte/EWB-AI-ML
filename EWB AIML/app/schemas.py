from typing import Optional
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    course: str
    marks: float = 0.0


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    course: Optional[str] = None
    marks: Optional[float] = None


class StudentOut(StudentCreate):
    id: int

    class Config:
        from_attributes = True


class AIQuery(BaseModel):
    question: str
