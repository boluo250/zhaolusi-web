from rest_framework import serializers
from .models import Photo, Video


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'file_path', 'category', 'description', 'created_at']
        

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file_path', 'embed_link', 'category', 'description', 'thumbnail', 'created_at']