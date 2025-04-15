from sqlalchemy.orm import Session
from app.models.models import Topic
from app.schemas.topic import TopicCreate


def get_topic(db: Session, topic_id: int):
    return db.query(Topic).filter(Topic.topic_id == topic_id).first()


def get_all_topics(db: Session):
    return db.query(Topic).all()


def create_topic(db: Session, topic_data: TopicCreate):
    new_topic = Topic(**topic_data.dict())
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic
