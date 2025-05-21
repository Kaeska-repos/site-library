from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Readers(models.Model):
    '''A model for registering readers.'''
    date_birth = models.DateField(verbose_name='Дата рождения')
    phone = models.IntegerField(validators=[RegexValidator(regex=r'^\d{10}$')], verbose_name='Телефон', unique=True)
    user = models.OneToOneField(User, models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

    def __str__(self):
        return f'{self.user} {self.phone} {self.date_birth}'