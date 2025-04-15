from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.topic import TopicCreate, TopicResponse
from app.crud import topic as crud_topic

router = APIRouter(prefix="/topics", tags=["Topic"])


@router.get("/", response_model=list[TopicResponse])
def get_all_topics(db: Session = Depends(get_db)):
    return crud_topic.get_all_topics(db)


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = crud_topic.get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.post("/", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    return crud_topic.create_topic(db, topic)
