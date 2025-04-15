from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import UserCreate
from app.utils.auth import hash_password


def create_user(db: Session, user_data: UserCreate):
    user = User(
        user_id=user_data.user_id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()
