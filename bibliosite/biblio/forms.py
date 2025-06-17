from django import forms

from .models import *
from bibliosite.widgets import Calendar

# Create your models here.
class UserChoice(forms.ModelChoiceField):
    '''Display the users first and last name in the drop-down list.'''
    def label_from_instance(self, obj):
        return f'{obj.last_name} {obj.first_name}'
    

class DistributionChoice(forms.ModelChoiceField):
    '''Display the users first and last name in the drop-down list.'''
    def label_from_instance(self, obj):
        return f'{obj.book} {obj.rental_date}'


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
    person = UserChoice(queryset=User.objects.filter(is_superuser=0), label='Имя')
    book = forms.ModelChoiceField(queryset=ListBooks.objects.filter(distribution=None), label='Книга')

    class Meta:
        model = Distribution
        fields = '__all__'
        widgets = {'rental_date': Calendar()}


class DistributionSelect(forms.Form):
    field = UserChoice(queryset=User.objects.filter(is_superuser=0), label='Выбрать читателя')


class DistributionDelete(forms.ModelForm):
    book = DistributionChoice(queryset=Distribution.objects.none(), label='Выданные книги')

    class Meta:
        model = Distribution
        fields = ['book']

    def __init__(self, *args, **kwargs):
        person_id = kwargs.pop('person_id', None)
        super().__init__(*args, **kwargs)
        if person_id:
            self.fields['book'].queryset = Distribution.objects.filter(person_id=person_id)