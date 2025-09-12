from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.TimelineEventListAPIView.as_view(), name='timeline-event-list'),
    path('events/<int:pk>/', views.TimelineEventDetailAPIView.as_view(), name='timeline-event-detail'),
    path('featured/', views.featured_events, name='featured-events'),
    path('years/', views.timeline_years, name='timeline-years'),
]