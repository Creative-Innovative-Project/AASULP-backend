from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.week import WeekCreate, WeekResponse
from app.crud import week as crud_week

router = APIRouter(prefix="/weeks", tags=["Week"])


@router.get("/", response_model=list[WeekResponse])
def get_all_weeks(db: Session = Depends(get_db)):
    return crud_week.get_all_weeks(db)


@router.get("/{week_id}", response_model=WeekResponse)
def get_week(week_id: int, db: Session = Depends(get_db)):
    week = crud_week.get_week(db, week_id)
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")
    return week


@router.post("/", response_model=WeekResponse)
def create_week(week: WeekCreate, db: Session = Depends(get_db)):
    return crud_week.create_week(db, week)
