from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import random
from core.database import engine
from models import Base
from routers import gallery_router, timeline_router
from routers.messages import router as messages_router

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
media_directory = os.path.abspath("../media")
if not os.path.exists(media_directory):
    os.makedirs(media_directory)
    
app.mount("/media", StaticFiles(directory=media_directory), name="media")

# Include routers
app.include_router(gallery_router, prefix="/api/gallery", tags=["gallery"])
app.include_router(timeline_router, prefix="/api/timeline", tags=["timeline"])
app.include_router(messages_router, prefix="/api", tags=["messages"])

@app.get("/")
def read_root():
    return {"message": "ZhaoLuSi Personal Website API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/random-hero-image")
def get_random_hero_image():
    """Get a random image from media/pic directory for hero section"""
    pic_dir = "/home/ubuntu/zhaolusi-web/media/pic"
    
    if not os.path.exists(pic_dir):
        return JSONResponse(
            status_code=404,
            content={"error": "Pictures directory not found"}
        )
    
    # Get all image files from pic directory
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    image_files = [
        f for f in os.listdir(pic_dir)
        if os.path.splitext(f.lower())[1] in image_extensions
    ]
    
    if not image_files:
        return JSONResponse(
            status_code=404,
            content={"error": "No images found in pictures directory"}
        )
    
    # Select a random image
    random_image = random.choice(image_files)
    image_url = f"/media/pic/{random_image}"
    
    return {
        "image_url": image_url,
        "filename": random_image
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)