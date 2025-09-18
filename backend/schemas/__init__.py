from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum

class CategoryEnum(str, Enum):
    travel = "travel"
    family = "family"
    life = "life"
    work = "work"
    other = "other"

class EventTypeEnum(str, Enum):
    milestone = "milestone"
    achievement = "achievement"
    travel = "travel"
    work = "work"
    education = "education"
    family = "family"
    other = "other"

class MessageStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Photo schemas
class PhotoBase(BaseModel):
    title: str = Field(..., max_length=200)
    file_path: str
    category: CategoryEnum = CategoryEnum.life
    description: Optional[str] = ""

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[CategoryEnum] = None
    description: Optional[str] = None

class PhotoResponse(PhotoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Video schemas
class VideoBase(BaseModel):
    title: str = Field(..., max_length=200)
    file_path: Optional[str] = ""
    embed_link: Optional[str] = ""
    category: CategoryEnum = CategoryEnum.life
    description: Optional[str] = ""
    thumbnail: Optional[str] = ""

class VideoCreate(VideoBase):
    pass

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    file_path: Optional[str] = None
    embed_link: Optional[str] = None
    category: Optional[CategoryEnum] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None

class VideoResponse(VideoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Timeline Event schemas
class TimelineEventBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    event_date: date
    event_type: EventTypeEnum = EventTypeEnum.other
    location: Optional[str] = ""
    image: Optional[str] = ""
    is_featured: bool = False

class TimelineEventCreate(TimelineEventBase):
    pass

class TimelineEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None
    event_type: Optional[EventTypeEnum] = None
    location: Optional[str] = None
    image: Optional[str] = None
    is_featured: Optional[bool] = None

class TimelineEventResponse(TimelineEventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Featured content response
class FeaturedContentResponse(BaseModel):
    photos: list[PhotoResponse]
    videos: list[VideoResponse]

class FeaturedEventsResponse(BaseModel):
    events: list[TimelineEventResponse]

# Statistics responses
class GalleryStatsResponse(BaseModel):
    photos: int
    videos: int
    photo_categories: int
    video_categories: int

class TimelineStatsResponse(BaseModel):
    years: list[int]
    total_events: int
    featured_events: int

class RandomHeroResponse(BaseModel):
    image_url: str

# Message schemas
class MessageBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)
    email: Optional[str] = ""

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    nickname: str
    content: str
    email: str
    status: MessageStatusEnum
    likes_count: int  # 添加点赞数量
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageAdminResponse(MessageResponse):
    ip_address: str
    spam_score: float
    approved_at: Optional[datetime]
    approved_by: str

class MessageUpdate(BaseModel):
    status: MessageStatusEnum
    approved_by: Optional[str] = None

class MessageStatsResponse(BaseModel):
    total_messages: int
    pending_messages: int
    approved_messages: int

# Message Like schemas
class MessageLikeResponse(BaseModel):
    id: int
    message_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True