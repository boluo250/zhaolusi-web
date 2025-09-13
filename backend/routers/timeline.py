from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from typing import List, Optional
from core.database import get_db
from models import TimelineEvent
from schemas import (
    TimelineEventResponse, TimelineEventCreate, TimelineEventUpdate,
    FeaturedEventsResponse, TimelineStatsResponse
)

router = APIRouter()

# Timeline event endpoints
@router.get("/events", response_model=List[TimelineEventResponse])
def get_timeline_events(
    event_type: Optional[str] = Query(None),
    is_featured: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(TimelineEvent)
    
    if event_type:
        query = query.filter(TimelineEvent.event_type == event_type)
    
    if is_featured is not None:
        query = query.filter(TimelineEvent.is_featured == is_featured)
    
    if search:
        query = query.filter(
            TimelineEvent.title.contains(search) | 
            TimelineEvent.description.contains(search) |
            TimelineEvent.location.contains(search)
        )
    
    events = query.order_by(TimelineEvent.event_date.desc()).offset(skip).limit(limit).all()
    return events

@router.get("/events/{event_id}", response_model=TimelineEventResponse)
def get_timeline_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    return event

@router.post("/events", response_model=TimelineEventResponse)
def create_timeline_event(event: TimelineEventCreate, db: Session = Depends(get_db)):
    db_event = TimelineEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/events/{event_id}", response_model=TimelineEventResponse)
def update_timeline_event(event_id: int, event_update: TimelineEventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/events/{event_id}")
def delete_timeline_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    
    db.delete(db_event)
    db.commit()
    return {"message": "Timeline event deleted successfully"}

# Featured events for homepage
@router.get("/featured", response_model=FeaturedEventsResponse)
def get_featured_events(db: Session = Depends(get_db)):
    events = db.query(TimelineEvent).filter(TimelineEvent.is_featured == True).limit(5).all()
    return FeaturedEventsResponse(events=events)

# Timeline statistics and years
@router.get("/stats", response_model=TimelineStatsResponse)
def get_timeline_stats(db: Session = Depends(get_db)):
    # Get distinct years from event_date
    years_result = db.query(extract('year', TimelineEvent.event_date)).distinct().all()
    years = [int(year[0]) for year in years_result]
    years.sort(reverse=True)
    
    total_events = db.query(TimelineEvent).count()
    featured_events = db.query(TimelineEvent).filter(TimelineEvent.is_featured == True).count()
    
    return TimelineStatsResponse(
        years=years,
        total_events=total_events,
        featured_events=featured_events
    )