import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class ListBooks(models.Model):
    '''A model for book registration.'''
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    author = models.CharField(max_length=60, verbose_name='Автор')
    year = models.IntegerField(validators=[MaxValueValidator(datetime.date.today().year)], verbose_name='Год издания')
    publisher = models.CharField(max_length=50, verbose_name='Издательство')
    edition = models.PositiveIntegerField(default=1, verbose_name='Номер издания')
    cover = models.ImageField(upload_to="covers/%Y/", blank=True, verbose_name='Обложка')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return f'{self.title} / {self.author}'
    

class NumberOfBooks(models.Model):
    number = models.PositiveIntegerField(verbose_name='Количество')
    additionally = models.TextField(max_length=1000, blank=True, verbose_name='Дополнительно')
    book = models.OneToOneField(ListBooks, models.CASCADE, verbose_name='Название книги / авторы')


class Distribution(models.Model):
    '''A model for managing the distribution of books to readers.'''
    rental_date = models.DateField(verbose_name='Дата выдачи')
    book = models.ForeignKey(ListBooks, models.CASCADE, verbose_name='Название книги / авторы')
    person = models.ForeignKey(User, models.CASCADE, verbose_name='Фамилия Имя гг-мм-дд рождения')

    class Meta:
        verbose_name = "Выдано книг"
        verbose_name_plural = "Выдано книг"

    def __str__(self):
        return f'{self.person}, книга: {self.book}'