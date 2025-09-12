from django.db import models


class Photo(models.Model):
    CATEGORY_CHOICES = [
        ('travel', '旅行'),
        ('family', '家人'),
        ('life', '生活'),
        ('work', '工作'),
        ('other', '其他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='标题')
    file_path = models.ImageField(upload_to='photos/', verbose_name='照片文件')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='life',
        verbose_name='分类'
    )
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '照片'
        verbose_name_plural = '照片'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('travel', '旅行'),
        ('family', '家人'),
        ('life', '生活'),
        ('work', '工作'),
        ('other', '其他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='标题')
    file_path = models.FileField(upload_to='videos/', blank=True, verbose_name='视频文件')
    embed_link = models.URLField(blank=True, verbose_name='嵌入链接')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='life',
        verbose_name='分类'
    )
    description = models.TextField(blank=True, verbose_name='描述')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, verbose_name='缩略图')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
