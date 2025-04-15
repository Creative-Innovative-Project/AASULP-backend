from pydantic import BaseModel
from typing import Optional


class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    resources: Optional[str] = None
    status: str  # Should be either "Pending" or "Completed"
    week_id: int


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    topic_id: int

    class Config:
        orm_mode = True
