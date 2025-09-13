from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from core.database import engine
from models import Base
from routers import gallery_router, timeline_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ZhaoLuSi Personal Website API",
    description="FastAPI backend for ZhaoLuSi personal website",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for media
if not os.path.exists("media"):
    os.makedirs("media")
    
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include routers
app.include_router(gallery_router, prefix="/api/gallery", tags=["gallery"])
app.include_router(timeline_router, prefix="/api/timeline", tags=["timeline"])

@app.get("/")
def read_root():
    return {"message": "ZhaoLuSi Personal Website API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)