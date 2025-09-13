from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./zhaolusi.db"
    media_root: str = "./media"
    media_url: str = "/media/"
    
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