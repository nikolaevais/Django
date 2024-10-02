from django.db import models

from users.models import NULLABLE

class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Содержимое статьи', **NULLABLE)
    image = models.ImageField(upload_to='blog/photo', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title', 'description']


