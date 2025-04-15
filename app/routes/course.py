from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.course import CourseCreate, CourseResponse
from app.crud import course as crud_course

router = APIRouter(prefix="/courses", tags=["Course"])


@router.get("/", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return crud_course.get_all_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud_course.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return crud_course.create_course(db, course)
