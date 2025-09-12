from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import TimelineEvent
from .serializers import TimelineEventSerializer


class TimelineEventListAPIView(generics.ListAPIView):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['event_type', 'is_featured']
    search_fields = ['title', 'description', 'location']


class TimelineEventDetailAPIView(generics.RetrieveAPIView):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer


@api_view(['GET'])
def featured_events(request):
    """Get featured timeline events for homepage"""
    events = TimelineEvent.objects.filter(is_featured=True)[:5]
    
    return Response({
        'events': TimelineEventSerializer(events, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
def timeline_years(request):
    """Get available years with events"""
    years = TimelineEvent.objects.dates('event_date', 'year', order='DESC')
    year_list = [year.year for year in years]
    
    return Response({
        'years': year_list,
        'total_events': TimelineEvent.objects.count(),
        'featured_events': TimelineEvent.objects.filter(is_featured=True).count(),
    })
