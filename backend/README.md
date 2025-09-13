# FastAPI Backend for ZhaoLuSi Personal Website

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── core/
│   ├── __init__.py
│   └── database.py        # Database configuration
├── models/
│   └── __init__.py        # SQLAlchemy models
├── schemas/
│   └── __init__.py        # Pydantic schemas
└── routers/
    ├── __init__.py
    ├── gallery.py         # Photo/Video API endpoints
    └── timeline.py        # Timeline events API endpoints
```

## Quick Start

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at http://localhost:8001

## API Documentation

- Interactive API docs: http://localhost:8001/docs
- OpenAPI schema: http://localhost:8001/openapi.json

## API Endpoints

### Gallery
- `GET /api/gallery/photos` - List photos with filtering
- `GET /api/gallery/photos/{id}` - Get photo by ID
- `POST /api/gallery/photos` - Create new photo
- `PUT /api/gallery/photos/{id}` - Update photo
- `DELETE /api/gallery/photos/{id}` - Delete photo
- `GET /api/gallery/videos` - List videos with filtering
- `GET /api/gallery/featured` - Get featured content
- `GET /api/gallery/stats` - Get gallery statistics
- `GET /api/gallery/random-hero` - Get random hero image

### Timeline
- `GET /api/timeline/events` - List timeline events with filtering
- `GET /api/timeline/events/{id}` - Get event by ID
- `POST /api/timeline/events` - Create new event
- `PUT /api/timeline/events/{id}` - Update event
- `DELETE /api/timeline/events/{id}` - Delete event
- `GET /api/timeline/featured` - Get featured events
- `GET /api/timeline/stats` - Get timeline statistics

## Database

Uses SQLite by default. Database file will be created as `zhaolusi.db` in the current directory.

## Media Files

Static media files are served from the `/media` endpoint. Create a `media` directory with subdirectories:
- `media/photos/` - Photo files
- `media/videos/` - Video files
- `media/video_thumbnails/` - Video thumbnails
- `media/timeline_images/` - Timeline event images
- `media/pic/` - Random hero images