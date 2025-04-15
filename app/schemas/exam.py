from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExamBase(BaseModel):
    title: str
    type: str  # Should be one of: "Assesment 1", "Assesment 2", "End Semester"
    rank: int
    start_date: date
    end_date: date
    status: str  # Should be one of: "Scheduled", "Completed"
    mark: Optional[float] = 0.0
    user_id: int
    course_id: int


class ExamCreate(ExamBase):
    pass


class ExamResponse(ExamBase):
    exam_id: int

    class Config:
        orm_mode = True
