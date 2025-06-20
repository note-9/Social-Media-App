from fastapi import HTTPException, Depends, status, APIRouter
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from models import User
from utils import hash_password
from database import get_db
from schemas import UserResponse, UserCreate

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_user_data = user.dict()
    hashed_user_data["password"] = hash_password(user.password)
    new_user = User(**hashed_user_data) # use the SQLAlchemy model
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # get auto-generated ID and timestamp
    return new_user

@router.get("/{id}", response_model = UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user
