from sqlalchemy.orm import Session
from app.models.models import Course
from app.schemas.course import CourseCreate


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.course_id == course_id).first()


def get_all_courses(db: Session):
    return db.query(Course).all()


def create_course(db: Session, course_data: CourseCreate):
    new_course = Course(**course_data.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
