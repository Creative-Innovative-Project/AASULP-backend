# app/schemas/semester.py

from pydantic import BaseModel
from typing import Optional


class SemesterBase(BaseModel):
    title: str
    user_id: int
    gpa: Optional[float] = None


class SemesterCreate(SemesterBase):
    pass


class SemesterResponse(SemesterBase):
    semester_id: int

    class Config:
        orm_mode = True
