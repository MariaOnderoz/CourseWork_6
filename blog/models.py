from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Модель блога"""

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг', **NULLABLE)
    content = models.TextField(verbose_name='Содержание', **NULLABLE)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_counter = models.PositiveIntegerField(default=0, verbose_name='Счетчик просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

