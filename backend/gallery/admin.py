from django.contrib import admin
from .models import Photo, Video


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'file_path', 'category')
        }),
        ('详细信息', {
            'fields': ('description',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'has_file', 'has_embed_link', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category')
        }),
        ('视频内容', {
            'fields': ('file_path', 'embed_link', 'thumbnail')
        }),
        ('详细信息', {
            'fields': ('description',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_file(self, obj):
        return bool(obj.file_path)
    has_file.boolean = True
    has_file.short_description = '本地视频'
    
    def has_embed_link(self, obj):
        return bool(obj.embed_link)
    has_embed_link.boolean = True
    has_embed_link.short_description = '嵌入链接'
