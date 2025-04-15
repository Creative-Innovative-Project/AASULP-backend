from sqlalchemy.orm import Session
from app.models.models import Exam
from app.schemas.exam import ExamCreate


def get_exam(db: Session, exam_id: int):
    return db.query(Exam).filter(Exam.exam_id == exam_id).first()


def get_all_exams(db: Session):
    return db.query(Exam).all()


def create_exam(db: Session, exam_data: ExamCreate):
    new_exam = Exam(**exam_data.dict())
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam
