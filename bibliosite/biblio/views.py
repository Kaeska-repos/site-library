from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ListBooks

# Create your views here.
class ListBooksPage(ListView):
    '''Displays a list of all books.'''
    model = ListBooks
    paginate_by = 10

class DetailBook(DetailView):
    '''Show full information about the book.'''
    model = ListBooks