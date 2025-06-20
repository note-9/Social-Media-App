from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class VoteSchema(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool

class PostResponse(PostCreate):
    id: int
    date: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

