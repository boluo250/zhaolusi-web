from rest_framework import serializers
from .models import TimelineEvent


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = [
            'id', 'title', 'description', 'event_date', 'event_type', 
            'location', 'image', 'is_featured', 'created_at'
        ]