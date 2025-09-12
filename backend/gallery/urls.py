from django.urls import path
from . import views

urlpatterns = [
    path('photos/', views.PhotoListAPIView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', views.PhotoDetailAPIView.as_view(), name='photo-detail'),
    path('videos/', views.VideoListAPIView.as_view(), name='video-list'),
    path('videos/<int:pk>/', views.VideoDetailAPIView.as_view(), name='video-detail'),
    path('featured/', views.featured_content, name='featured-content'),
    path('stats/', views.gallery_stats, name='gallery-stats'),
]