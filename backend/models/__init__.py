from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)  # Store file path as string
    category = Column(String(20), default="life")
    description = Column(Text, default="")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    file_path = Column(String(500), default="")  # Local video file
    embed_link = Column(String(500), default="")  # External video link
    category = Column(String(20), default="life")
    description = Column(Text, default="")
    thumbnail = Column(String(500), default="")  # Thumbnail image path
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    event_type = Column(String(20), default="other")
    location = Column(String(200), default="")
    image = Column(String(500), default="")  # Related image path
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    email = Column(String(100), default="")  # Optional for reply notification
    ip_address = Column(String(45), nullable=False)  # For spam protection
    status = Column(String(20), default="pending")  # pending, approved, rejected
    spam_score = Column(Float, default=0.0)  # Auto spam detection score
    likes_count = Column(Integer, default=0)  # 点赞数量
    created_at = Column(DateTime, default=func.now())
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(String(50), default="")

class MessageLike(Base):
    __tablename__ = "message_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    ip_address = Column(String(45), nullable=False)  # 用IP限制重复点赞
    created_at = Column(DateTime, default=func.now())

class BannedWord(Base):
    __tablename__ = "banned_words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False)
    severity = Column(String(10), default="medium")  # low, medium, high
    created_at = Column(DateTime, default=func.now())