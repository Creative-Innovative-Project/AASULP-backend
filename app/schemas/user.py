from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr  # Validates email format
    password: str


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True
