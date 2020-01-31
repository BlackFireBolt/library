from django.db import models
from django.urls import reverse

from storages.backends.sftpstorage import SFTPStorage 

sfs = SFTPStorage()

class Category(models.Model):
    name = models.CharField(max_length = 100, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Факультет')

class SuperCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)

class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)

class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return '%s - %s' % (self.super_category.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_category__order', 'super_category__name', 'order', 'name')
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

class Author(models.Model):
    name = models.CharField(max_length=20, verbose_name='Фамилия и инициалы автора')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Publisher(models.Model):
    name = models.CharField(max_length=20, verbose_name='Издатель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'


class Topic(models.Model):
    title = models.CharField(max_length=30, verbose_name='Предмет обсуждения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
    


class Article(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name='Кафедра')
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.ManyToManyField(Author, verbose_name='Автор')
    compiler = models.BooleanField(default=False,verbose_name='Составитель')
    publisher = models.ForeignKey(Publisher, blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Издатель')
    publishing_house = models.CharField(blank=True, max_length=1024, verbose_name='Издательство')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name='Тема')
    description = models.TextField(verbose_name='Аннотация')
    bibliographic_description = models.TextField(blank=True, verbose_name='Библиографическое описание')
    publication_year = models.IntegerField(choices=[(r,r) for r in range(1950, 2030)], default='Выберите год', verbose_name='Год публикации')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    isbn = models.CharField(blank=True, max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                            verbose_name='ISBN')

    file = models.FileField(upload_to='articles/', storage=sfs, verbose_name='Файл')
    image = models.ImageField(blank=True, upload_to='image/magazines', storage=sfs, verbose_name='Изображение') 

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('created_at',)