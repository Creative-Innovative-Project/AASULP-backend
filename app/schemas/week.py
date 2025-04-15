from pydantic import BaseModel
from typing import Optional


class WeekBase(BaseModel):
    title: str
    rank: int
    course_id: int
    quiz_id: Optional[int] = None
    user_id: int
    status: Optional[str] = "Ongoing"
    attendance: Optional[float] = 0.0


class WeekCreate(WeekBase):
    pass


class WeekResponse(WeekBase):
    week_id: int

    class Config:
        orm_mode = True
