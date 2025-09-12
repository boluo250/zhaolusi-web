from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Video
from .serializers import PhotoSerializer, VideoSerializer


class PhotoListAPIView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']


class PhotoDetailAPIView(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']


class VideoDetailAPIView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


@api_view(['GET'])
def featured_content(request):
    """Get featured photos and videos for homepage"""
    photos = Photo.objects.all()[:6]
    videos = Video.objects.all()[:4]
    
    return Response({
        'photos': PhotoSerializer(photos, many=True, context={'request': request}).data,
        'videos': VideoSerializer(videos, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
def gallery_stats(request):
    """Get gallery statistics"""
    photo_count = Photo.objects.count()
    video_count = Video.objects.count()
    photo_categories = Photo.objects.values('category').distinct().count()
    video_categories = Video.objects.values('category').distinct().count()
    
    return Response({
        'photos': photo_count,
        'videos': video_count,
        'photo_categories': photo_categories,
        'video_categories': video_categories,
    })
