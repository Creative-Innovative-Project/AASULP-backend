from pydantic import BaseModel
from typing import Optional
from datetime import date


class CourseBase(BaseModel):
    title: str
    credit: int
    periods: int
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = "Active"
    mark: Optional[float] = 0.0
    attendance: Optional[float] = 0.0
    user_id: int
    semester_id: int


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    course_id: int

    class Config:
        orm_mode = True
