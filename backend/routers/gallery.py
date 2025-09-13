from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import random
from core.database import get_db, settings
from models import Photo, Video
from schemas import (
    PhotoResponse, VideoResponse, PhotoCreate, VideoCreate,
    PhotoUpdate, VideoUpdate, FeaturedContentResponse,
    GalleryStatsResponse, RandomHeroResponse
)

router = APIRouter()

# Photo endpoints
@router.get("/photos", response_model=List[PhotoResponse])
def get_photos(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(Photo)
    
    if category:
        query = query.filter(Photo.category == category)
    
    if search:
        query = query.filter(Photo.title.contains(search) | Photo.description.contains(search))
    
    photos = query.offset(skip).limit(limit).all()
    return photos

@router.get("/photos/{photo_id}", response_model=PhotoResponse)
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

@router.post("/photos", response_model=PhotoResponse)
def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = Photo(**photo.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.put("/photos/{photo_id}", response_model=PhotoResponse)
def update_photo(photo_id: int, photo_update: PhotoUpdate, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    update_data = photo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_photo, field, value)
    
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.delete("/photos/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    db.delete(db_photo)
    db.commit()
    return {"message": "Photo deleted successfully"}

# Video endpoints
@router.get("/videos", response_model=List[VideoResponse])
def get_videos(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(Video)
    
    if category:
        query = query.filter(Video.category == category)
    
    if search:
        query = query.filter(Video.title.contains(search) | Video.description.contains(search))
    
    videos = query.offset(skip).limit(limit).all()
    return videos

@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/videos", response_model=VideoResponse)
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    db_video = Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

@router.put("/videos/{video_id}", response_model=VideoResponse)
def update_video(video_id: int, video_update: VideoUpdate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    update_data = video_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_video, field, value)
    
    db.commit()
    db.refresh(db_video)
    return db_video

@router.delete("/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db.delete(db_video)
    db.commit()
    return {"message": "Video deleted successfully"}

# Featured content for homepage
@router.get("/featured", response_model=FeaturedContentResponse)
def get_featured_content(db: Session = Depends(get_db)):
    photos = db.query(Photo).limit(6).all()
    videos = db.query(Video).limit(4).all()
    
    return FeaturedContentResponse(photos=photos, videos=videos)

# Gallery statistics
@router.get("/stats", response_model=GalleryStatsResponse)
def get_gallery_stats(db: Session = Depends(get_db)):
    photo_count = db.query(Photo).count()
    video_count = db.query(Video).count()
    photo_categories = db.query(func.count(func.distinct(Photo.category))).scalar()
    video_categories = db.query(func.count(func.distinct(Video.category))).scalar()
    
    return GalleryStatsResponse(
        photos=photo_count,
        videos=video_count,
        photo_categories=photo_categories,
        video_categories=video_categories
    )

# Wall photos for featured section
@router.get("/wall-photos")
def get_wall_photos():
    wall_pic_dir = os.path.join(settings.media_root, 'wall-pic')
    
    try:
        if os.path.exists(wall_pic_dir):
            image_files = [f for f in os.listdir(wall_pic_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            if image_files:
                # 随机打乱照片顺序
                random.shuffle(image_files)
                wall_photos = []
                for image_file in image_files:
                    wall_photos.append({
                        "filename": image_file,
                        "url": f"{settings.media_url}wall-pic/{image_file}"
                    })
                return {"photos": wall_photos}
            else:
                return {"photos": []}
        else:
            raise HTTPException(status_code=404, detail="Wall-pic directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Random hero image
@router.get("/random-hero", response_model=RandomHeroResponse)
def get_random_hero_image():
    pic_dir = os.path.join(settings.media_root, 'pic')
    
    try:
        if os.path.exists(pic_dir):
            image_files = [f for f in os.listdir(pic_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            if image_files:
                random_image = random.choice(image_files)
                image_url = f"{settings.media_url}pic/{random_image}"
                return RandomHeroResponse(image_url=image_url)
            else:
                raise HTTPException(status_code=404, detail="No images found")
        else:
            raise HTTPException(status_code=404, detail="Image directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))