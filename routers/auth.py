from fastapi import APIRouter, status, HTTPException, Response, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils import hash_password, verify_password
from oauth2 import create_access_token
from schemas import Token,UserLogin

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    payload = {"user_id": user.id}
    access_token = create_access_token(payload=payload)
    return {"access_token": access_token, "token_type": "bearer"}