from sqlalchemy.orm import Session
from app.models.models import Week
from app.schemas.week import WeekCreate


def get_week(db: Session, week_id: int):
    return db.query(Week).filter(Week.week_id == week_id).first()


def get_all_weeks(db: Session):
    return db.query(Week).all()


def create_week(db: Session, week_data: WeekCreate):
    new_week = Week(**week_data.dict())
    db.add(new_week)
    db.commit()
    db.refresh(new_week)
    return new_week
