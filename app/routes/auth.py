from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.models import User
from app.dependencies import get_db
from app.utils.auth import verify_password, create_access_token
from datetime import timedelta

router = APIRouter()


class LoginRequest(BaseModel):
    user_id: str
    password: str


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == req.user_id).first()
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "user_name": user.first_name + " " + user.last_name,
    }
