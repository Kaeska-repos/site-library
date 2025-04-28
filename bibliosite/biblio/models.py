import datetime
from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator

# Create your models here.
class ListBooks(models.Model):
    '''A model for book registration.'''
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    author = models.CharField(max_length=60, verbose_name='Автор')
    year = models.IntegerField(validators=[MaxValueValidator(datetime.date.today().year)], verbose_name='Год издания')
    publisher = models.CharField(max_length=50, verbose_name='Издательство')
    edition = models.PositiveIntegerField(default=1, verbose_name='Номер издания')
    additionally = models.TextField(max_length=1000, blank=True, verbose_name='Дополнительно')
    cover = models.ImageField(upload_to="covers/%Y/", blank=True, verbose_name='Обложка')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f'{self.title} / {self.author}'


class Readers(models.Model):
    '''A model for registering readers.'''
    surname = models.CharField(max_length=40, verbose_name='Фамилия')
    name = models.CharField(max_length=20, verbose_name='Имя')
    date_birth = models.DateField(verbose_name='Дата рождения')
    phone = models.IntegerField(primary_key=True, validators=[RegexValidator(regex=r'^\d{10}$')], verbose_name='Телефон')

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

    def __str__(self):
        return f'{self.surname} {self.name} {self.date_birth}'


class Distribution(models.Model):
    '''A model for managing the distribution of books to readers.'''
    rental_date = models.DateField(verbose_name='Дата выдачи')
    book = models.OneToOneField(ListBooks, models.CASCADE, verbose_name='Название книги / авторы')
    person = models.OneToOneField(Readers, models.CASCADE, verbose_name='Фамилия Имя гг-мм-дд рождения')

    class Meta:
        verbose_name = "Выдано книг"
        verbose_name_plural = "Выдано книг"

    def __str__(self):
        return f'{self.person}, книга: {self.book}'
