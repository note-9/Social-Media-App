from fastapi import HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Post, Vote, User
from database import get_db
from oauth2 import get_current_user
from schemas import PostCreate,PostResponse,UserResponse, PostOut

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/{id}", response_model = PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return post

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.id, **post.dict())  # use the SQLAlchemy model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # get auto-generated ID and timestamp
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    db.delete(post)
    db.commit()
    return

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post_data: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    post.title = post_data.title
    post.content = post_data.content
    post.published = post_data.published
    db.commit()
    db.refresh(post)
    return post