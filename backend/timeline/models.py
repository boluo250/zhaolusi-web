from django.db import models


class TimelineEvent(models.Model):
    EVENT_TYPES = [
        ('milestone', '人生里程碑'),
        ('achievement', '成就'),
        ('travel', '旅行'),
        ('work', '工作'),
        ('education', '教育'),
        ('family', '家庭'),
        ('other', '其他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='事件标题')
    description = models.TextField(verbose_name='事件描述')
    event_date = models.DateField(verbose_name='事件日期')
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='other',
        verbose_name='事件类型'
    )
    location = models.CharField(max_length=200, blank=True, verbose_name='地点')
    image = models.ImageField(upload_to='timeline_images/', blank=True, verbose_name='相关图片')
    is_featured = models.BooleanField(default=False, verbose_name='是否为重要事件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '人生轨迹事件'
        verbose_name_plural = '人生轨迹事件'
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.event_date.year}年 - {self.title}"
