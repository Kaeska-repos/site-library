from django import forms

# Create your models here.
class FindBook(forms.Form):
    '''A form for searching for books in the list.'''
    title = forms.CharField(max_length=100, label='Название (обязательно)', required=False)
    author = forms.CharField(max_length=60, label='Автор', required=False)