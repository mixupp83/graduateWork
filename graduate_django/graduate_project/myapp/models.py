from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    content = models.TextField(verbose_name='Содержание (контент)')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title