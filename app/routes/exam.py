from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.exam import ExamCreate, ExamResponse
from app.crud import exam as crud_exam

router = APIRouter(prefix="/exams", tags=["Exam"])


@router.get("/", response_model=list[ExamResponse])
def get_all_exams(db: Session = Depends(get_db)):
    return crud_exam.get_all_exams(db)


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = crud_exam.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.post("/", response_model=ExamResponse)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    return crud_exam.create_exam(db, exam)
