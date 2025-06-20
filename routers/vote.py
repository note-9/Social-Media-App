from fastapi import HTTPException, Depends, status, APIRouter
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from models import User, Vote, Post
from utils import hash_password
from database import get_db
from oauth2 import get_current_user
from schemas import UserResponse, UserCreate, VoteSchema

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote: VoteSchema, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote Added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Vote Deleted"}
