from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session
    finally:
        db.close()  # Close the session after request
