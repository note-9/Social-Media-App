from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

load_dotenv()  # load from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return id

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token).first()
    return user