# app/crud/semester.py

from sqlalchemy.orm import Session
from app.models.models import Semester
from app.schemas.semester import SemesterCreate


def get_semester(db: Session, semester_id: int):
    return db.query(Semester).filter(Semester.semester_id == semester_id).first()


def get_all_semesters(db: Session):
    return db.query(Semester).all()


def create_semester(db: Session, semester: SemesterCreate):
    db_sem = Semester(**semester.dict())
    db.add(db_sem)
    db.commit()
    db.refresh(db_sem)
    return db_sem
