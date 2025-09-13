from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from typing import Optional
from fastapi import HTTPException, Header
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./zhaolusi.db"
    media_root: str = os.path.abspath("../media")
    media_url: str = "/media/"
    admin_api_key: str = "your-secure-admin-key-change-this"  # 管理员API密钥
    
    class Config:
        env_file = ".env"

settings = Settings()

# Database setup
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin authentication dependency
def verify_admin_key(x_api_key: str = Header(...)):
    """Verify admin API key from header"""
    if x_api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True