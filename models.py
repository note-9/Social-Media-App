from database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title =  Column(String(50), nullable=False)
    content =  Column(String(500), nullable=False)
    published = Column(Boolean, default=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

Base.metadata.create_all(bind=engine)
