import datetime
from django.db import models
from django.core.validators import MaxValueValidator

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