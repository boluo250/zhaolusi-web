from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import re
import datetime
from core.database import get_db, verify_admin_key
from models import Message, BannedWord
from schemas import (
    MessageCreate, MessageResponse, MessageAdminResponse, 
    MessageUpdate, MessageStatsResponse
)

router = APIRouter()

# Spam detection helper functions
def calculate_spam_score(content: str, nickname: str, db: Session) -> float:
    """Calculate spam score based on content analysis"""
    score = 0.0
    
    # Check banned words
    banned_words = db.query(BannedWord).all()
    content_lower = content.lower()
    nickname_lower = nickname.lower()
    
    for banned_word in banned_words:
        word_lower = banned_word.word.lower()
        if word_lower in content_lower or word_lower in nickname_lower:
            if banned_word.severity == "high":
                score += 0.8
            elif banned_word.severity == "medium":
                score += 0.5
            else:
                score += 0.2
    
    # Check for excessive special characters
    special_chars = len(re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', content))
    if special_chars > len(content) * 0.3:
        score += 0.3
    
    # Check for excessive uppercase
    if content.isupper() and len(content) > 10:
        score += 0.2
    
    # Check for repeated characters
    if re.search(r'(.)\1{4,}', content):
        score += 0.3
    
    # Check for URLs (basic detection)
    if re.search(r'https?://|www\.', content.lower()):
        score += 0.4
    
    return min(score, 1.0)

def check_rate_limit(ip_address: str, db: Session) -> bool:
    """Check if IP is rate limited (max 3 messages per 10 minutes)"""
    ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
    recent_messages = db.query(Message).filter(
        Message.ip_address == ip_address,
        Message.created_at >= ten_minutes_ago
    ).count()
    
    return recent_messages >= 3

# Public endpoints
@router.post("/messages", response_model=dict)
def create_message(message: MessageCreate, request: Request, db: Session = Depends(get_db)):
    """Submit a new message (public endpoint)"""
    client_ip = request.client.host
    
    # Rate limiting
    if check_rate_limit(client_ip, db):
        raise HTTPException(status_code=429, detail="Too many messages. Please wait before submitting again.")
    
    # Calculate spam score
    spam_score = calculate_spam_score(message.content, message.nickname, db)
    
    # Auto-reject if spam score is too high
    status = "rejected" if spam_score >= 0.8 else "pending"
    
    # Create message
    db_message = Message(
        nickname=message.nickname,
        content=message.content,
        email=message.email,
        ip_address=client_ip,
        status=status,
        spam_score=spam_score
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return {
        "message": "留言已提交，等待审核后显示" if status == "pending" else "留言内容不符合要求，已被自动拒绝",
        "status": status
    }

@router.get("/messages", response_model=List[MessageResponse])
def get_approved_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get approved messages (public endpoint)"""
    messages = db.query(Message).filter(
        Message.status == "approved"
    ).order_by(
        Message.approved_at.desc()
    ).offset(skip).limit(limit).all()
    
    return messages

@router.get("/messages/stats", response_model=MessageStatsResponse)
def get_message_stats(db: Session = Depends(get_db)):
    """Get message statistics (public endpoint)"""
    total = db.query(Message).count()
    pending = db.query(Message).filter(Message.status == "pending").count()
    approved = db.query(Message).filter(Message.status == "approved").count()
    
    return MessageStatsResponse(
        total_messages=total,
        pending_messages=pending,
        approved_messages=approved
    )

# Admin endpoints (protected with API key)
@router.get("/admin/messages", response_model=List[MessageAdminResponse])
def get_all_messages_admin(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_key)
):
    """Get all messages for admin review (requires API key)"""
    query = db.query(Message)
    
    if status:
        query = query.filter(Message.status == status)
    
    messages = query.order_by(
        Message.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return messages

@router.put("/admin/messages/{message_id}/approve", response_model=MessageAdminResponse)
def approve_message(message_id: int, db: Session = Depends(get_db), admin_verified: bool = Depends(verify_admin_key)):
    """Approve a message (requires API key)"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = "approved"
    message.approved_at = datetime.datetime.now()
    message.approved_by = "admin"  # In real app, get from authentication
    
    db.commit()
    db.refresh(message)
    
    return message

@router.put("/admin/messages/{message_id}/reject", response_model=MessageAdminResponse)
def reject_message(message_id: int, db: Session = Depends(get_db), admin_verified: bool = Depends(verify_admin_key)):
    """Reject a message (requires API key)"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = "rejected"
    message.approved_by = "admin"
    
    db.commit()
    db.refresh(message)
    
    return message

@router.delete("/admin/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), admin_verified: bool = Depends(verify_admin_key)):
    """Delete a message (requires API key)"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    
    return {"message": "Message deleted successfully"}

# Banned words management
@router.post("/admin/banned-words")
def add_banned_word(word: str, severity: str = "medium", db: Session = Depends(get_db), admin_verified: bool = Depends(verify_admin_key)):
    """Add a banned word (requires API key)"""
    banned_word = BannedWord(word=word, severity=severity)
    db.add(banned_word)
    db.commit()
    return {"message": f"Banned word '{word}' added successfully"}

@router.get("/admin/banned-words")
def get_banned_words(db: Session = Depends(get_db), admin_verified: bool = Depends(verify_admin_key)):
    """Get all banned words (requires API key)"""
    return db.query(BannedWord).all()