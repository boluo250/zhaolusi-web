from django.contrib import admin
from .models import TimelineEvent


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_type', 'location', 'is_featured')
    list_filter = ('event_type', 'is_featured', 'event_date')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('事件信息', {
            'fields': ('title', 'description', 'event_date', 'event_type')
        }),
        ('地点和图片', {
            'fields': ('location', 'image')
        }),
        ('显示设置', {
            'fields': ('is_featured',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_not_featured']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"已将 {queryset.count()} 个事件标记为重要事件")
    mark_as_featured.short_description = "标记为重要事件"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"已将 {queryset.count()} 个事件取消重要标记")
    mark_as_not_featured.short_description = "取消重要事件标记"
