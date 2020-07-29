from django.db import models
from storages.backends.sftpstorage import SFTPStorage

sfs = SFTPStorage()


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    publication_date = models.DateField(verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', ]


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость')
    file = models.FileField(blank=True, upload_to='news_archive/', storage=sfs, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Иллюстрация'
        verbose_name_plural = 'Иллюстрации'
