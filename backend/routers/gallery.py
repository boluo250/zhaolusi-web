from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import random
import re
from datetime import datetime
from core.database import get_db, settings
from models import Photo, Video
from schemas import (
    PhotoResponse, VideoResponse, PhotoCreate, VideoCreate,
    PhotoUpdate, VideoUpdate, FeaturedContentResponse,
    GalleryStatsResponse, RandomHeroResponse
)

router = APIRouter()

# 解析文件名中的日期信息
def parse_filename_date(filename):
    """
    解析文件名中的日期，支持格式：YYYY年MM月DD日N.jpg
    例如：2025年08月16日1.jpg -> 2025-08-16
    """
    try:
        # 匹配 YYYY年MM月DD日N.jpg 格式
        pattern = r'(\d{4})年(\d{2})月(\d{2})日'
        match = re.search(pattern, filename)
        
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return datetime(year, month, day)
    except ValueError:
        pass
    
    return None

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
                # 解析文件名中的日期并排序
                wall_photos = []
                for image_file in image_files:
                    photo_date = parse_filename_date(image_file)
                    wall_photos.append({
                        "filename": image_file,
                        "url": f"{settings.media_url}wall-pic/{image_file}",
                        "date": photo_date.isoformat() if photo_date else None
                    })
                
                # 按日期排序（最新的在前）
                wall_photos.sort(key=lambda x: x["date"] or "1900-01-01", reverse=True)
                return {"photos": wall_photos}
            else:
                return {"photos": []}
        else:
            raise HTTPException(status_code=404, detail="Wall-pic directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get available years in wall-pic directory
@router.get("/wall-photos/years")
def get_wall_photo_years():
    wall_pic_dir = os.path.join(settings.media_root, 'wall-pic')
    
    try:
        if not os.path.exists(wall_pic_dir):
            raise HTTPException(status_code=404, detail="Wall-pic directory not found")
        
        image_files = [f for f in os.listdir(wall_pic_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        # 按文件名解析年份
        years_count = {}
        for image_file in image_files:
            photo_date = parse_filename_date(image_file)
            if photo_date:
                year = photo_date.year
                years_count[year] = years_count.get(year, 0) + 1
        
        # 生成年份数据
        years = []
        for year, count in years_count.items():
            years.append({
                "year": year,
                "photo_count": count
            })
        
        # 按年份降序排列
        years.sort(key=lambda x: x["year"], reverse=True)
        return {"years": years}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get photos by year and optionally by month
@router.get("/wall-photos/{year}")
def get_wall_photos_by_year(
    year: int,
    month: Optional[int] = Query(None, ge=1, le=12)
):
    wall_pic_dir = os.path.join(settings.media_root, 'wall-pic')
    
    try:
        if not os.path.exists(wall_pic_dir):
            raise HTTPException(status_code=404, detail=f"Wall-pic directory not found")
        
        image_files = [f for f in os.listdir(wall_pic_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not image_files:
            return {"photos": [], "months": []}
        
        # 按文件名解析日期，筛选指定年份的照片
        photos_by_month = {}
        for image_file in image_files:
            photo_date = parse_filename_date(image_file)
            if photo_date and photo_date.year == year:
                file_month = photo_date.month
                
                if file_month not in photos_by_month:
                    photos_by_month[file_month] = []
                
                photos_by_month[file_month].append({
                    "filename": image_file,
                    "url": f"{settings.media_url}wall-pic/{image_file}",
                    "date": photo_date.isoformat()
                })
        
        # 按月份排序照片（最新的在前）
        for month_photos in photos_by_month.values():
            month_photos.sort(key=lambda x: x["date"], reverse=True)
        
        # 生成月份统计
        months = []
        for month_num in sorted(photos_by_month.keys(), reverse=True):
            months.append({
                "month": month_num,
                "photo_count": len(photos_by_month[month_num])
            })
        
        # 如果指定了月份，只返回该月份的照片
        if month:
            if month in photos_by_month:
                return {
                    "photos": photos_by_month[month],
                    "months": months,
                    "year": year,
                    "selected_month": month
                }
            else:
                return {
                    "photos": [],
                    "months": months,
                    "year": year,
                    "selected_month": month
                }
        
        # 返回所有照片，按月份分组
        all_photos = []
        for month_num in sorted(photos_by_month.keys(), reverse=True):
            all_photos.extend(photos_by_month[month_num])
        
        return {
            "photos": all_photos,
            "photos_by_month": photos_by_month,
            "months": months,
            "year": year
        }
    
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

# 解析微博文件名中的日期信息
def parse_weibo_filename_date(filename):
    """
    解析微博文件名中的日期，支持格式：YYYY-MM-DD.jpg 或 YYYY-MM-DD-N.jpg
    例如：2015-11-12.jpg -> 2015-11-12
    """
    try:
        # 匹配 YYYY-MM-DD 格式
        pattern = r'(\d{4})-(\d{2})-(\d{2})'
        match = re.search(pattern, filename)
        
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return datetime(year, month, day)
    except ValueError:
        pass
    
    return None

# Weibo photos endpoints
@router.get("/weibo-photos")
def get_weibo_photos():
    weibo_dir = os.path.join(settings.media_root, 'weibo')
    
    try:
        if os.path.exists(weibo_dir):
            image_files = [f for f in os.listdir(weibo_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            
            if image_files:
                # 解析文件名中的日期并排序
                weibo_photos = []
                for image_file in image_files:
                    photo_date = parse_weibo_filename_date(image_file)
                    weibo_photos.append({
                        "filename": image_file,
                        "url": f"{settings.media_url}weibo/{image_file}",
                        "date": photo_date.isoformat() if photo_date else None
                    })
                
                # 按日期排序（最新的在前）
                weibo_photos.sort(key=lambda x: x["date"] or "1900-01-01", reverse=True)
                return {"photos": weibo_photos}
            else:
                return {"photos": []}
        else:
            raise HTTPException(status_code=404, detail="Weibo directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get available years in weibo directory
@router.get("/weibo-photos/years")
def get_weibo_photo_years():
    weibo_dir = os.path.join(settings.media_root, 'weibo')
    
    try:
        if not os.path.exists(weibo_dir):
            raise HTTPException(status_code=404, detail="Weibo directory not found")
        
        image_files = [f for f in os.listdir(weibo_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        # 按文件名解析年份
        years_count = {}
        for image_file in image_files:
            photo_date = parse_weibo_filename_date(image_file)
            if photo_date:
                year = photo_date.year
                years_count[year] = years_count.get(year, 0) + 1
        
        # 生成年份数据
        years = []
        for year, count in years_count.items():
            years.append({
                "year": year,
                "photo_count": count
            })
        
        # 按年份降序排列
        years.sort(key=lambda x: x["year"], reverse=True)
        return {"years": years}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get weibo photos by year and optionally by month
@router.get("/weibo-photos/{year}")
def get_weibo_photos_by_year(
    year: int,
    month: Optional[int] = Query(None, ge=1, le=12)
):
    weibo_dir = os.path.join(settings.media_root, 'weibo')
    
    try:
        if not os.path.exists(weibo_dir):
            raise HTTPException(status_code=404, detail=f"Weibo directory not found")
        
        image_files = [f for f in os.listdir(weibo_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not image_files:
            return {"photos": [], "months": []}
        
        # 按文件名解析日期，筛选指定年份的照片
        photos_by_month = {}
        for image_file in image_files:
            photo_date = parse_weibo_filename_date(image_file)
            if photo_date and photo_date.year == year:
                file_month = photo_date.month
                
                if file_month not in photos_by_month:
                    photos_by_month[file_month] = []
                
                photos_by_month[file_month].append({
                    "filename": image_file,
                    "url": f"{settings.media_url}weibo/{image_file}",
                    "date": photo_date.isoformat()
                })
        
        # 按月份排序照片（最新的在前）
        for month_photos in photos_by_month.values():
            month_photos.sort(key=lambda x: x["date"], reverse=True)
        
        # 生成月份统计
        months = []
        for month_num in sorted(photos_by_month.keys(), reverse=True):
            months.append({
                "month": month_num,
                "photo_count": len(photos_by_month[month_num])
            })
        
        # 如果指定了月份，只返回该月份的照片
        if month:
            if month in photos_by_month:
                return {
                    "photos": photos_by_month[month],
                    "months": months,
                    "year": year,
                    "selected_month": month
                }
            else:
                return {
                    "photos": [],
                    "months": months,
                    "year": year,
                    "selected_month": month
                }
        
        # 返回所有照片，按月份分组
        all_photos = []
        for month_num in sorted(photos_by_month.keys(), reverse=True):
            all_photos.extend(photos_by_month[month_num])
        
        return {
            "photos": all_photos,
            "photos_by_month": photos_by_month,
            "months": months,
            "year": year
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))