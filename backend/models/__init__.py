from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
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