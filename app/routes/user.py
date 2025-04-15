from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user
from app.dependencies import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, user.user_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_api(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
