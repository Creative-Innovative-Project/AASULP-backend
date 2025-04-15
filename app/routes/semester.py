# app/routes/semester.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.semester import SemesterCreate, SemesterResponse
from app.crud import semester as semester_crud
from app.dependencies import get_db

router = APIRouter()


@router.get("/semesters/{semester_id}", response_model=SemesterResponse)
def read_semester(semester_id: int, db: Session = Depends(get_db)):
    semester = semester_crud.get_semester(db, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@router.get("/semesters", response_model=list[SemesterResponse])
def read_all_semesters(db: Session = Depends(get_db)):
    return semester_crud.get_all_semesters(db)


@router.post("/semesters", response_model=SemesterResponse)
def create_new_semester(semester: SemesterCreate, db: Session = Depends(get_db)):
    return semester_crud.create_semester(db, semester)
