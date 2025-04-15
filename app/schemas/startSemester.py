from pydantic import BaseModel
from typing import List


class Elective(BaseModel):
    title: str
    option: str
    code: str


class StartSemesterData(BaseModel):
    user_id: int
    semester_title: str
    start_date: str
    end_date: str
    electives: List[Elective]
