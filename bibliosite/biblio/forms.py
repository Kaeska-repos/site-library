from django import forms

from .models import *
from bibliosite.widgets import Calendar

# Create your models here.
class FindBook(forms.Form):
    '''A form for searching for books in the list.'''
    title = forms.CharField(max_length=100, label='Название (обязательно)', required=False)
    author = forms.CharField(max_length=60, label='Автор', required=False)


class RegisterBook(forms.ModelForm):
    '''A form for book registration.'''
    class Meta:
        model = ListBooks
        fields = '__all__'


class DistributionForm(forms.ModelForm):
    '''The form for registration of giving the book to the reader.'''
    person = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=0), label='Имя')
    book = forms.ModelChoiceField(queryset=ListBooks.objects.filter(distribution=None), label='Книга')

    class Meta:
        model = Distribution
        fields = '__all__'
        widgets = {'rental_date': Calendar()}