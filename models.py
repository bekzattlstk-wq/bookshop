# Китептер, жанрлар, товарлар жана категориялар үчүн маалымат базасынын түзүмүн аныктайт.
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True, verbose_name= 'URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True, verbose_name= 'URL')
    category = models.ForeignKey('category', on_delete = models.CASCADE, related_name = 'products')
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    description = models.TextField(verbose_name='Описание',blank=True)
    image = models.ImageField(upload_to = 'products/%Y/%m', blank = True)
    is_available = models.BooleanField(default = True, verbose_name='В наличии')



class Genre(models.Model):
    name = models.CharField(max_length = 100, unique = True, verbose_name = 'Название жанра')
    slug = models.SlugField(max_length=100, unique = True, verbose_name= 'URL')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанр'
        ordering = ['name']

    def __str__(self):
        return self.name



class Book(models.Model):

    title = models.CharField(max_length=100, verbose_name = 'Имя книги')

    slug = models.SlugField(max_length=100, unique = True, verbose_name= 'URL')

    content = models.TextField(verbose_name= 'О книге')

    genres = models.ManyToManyField(Genre, related_name = 'books', blank = True, verbose_name = 'Жанры')

    image = models.ImageField(upload_to = 'books/%Y/%m/%d/',blank = True,null = True,verbose_name= 'Изображение')

    is_published = models.BooleanField(default = True, verbose_name = 'Опубликовано')

    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})



