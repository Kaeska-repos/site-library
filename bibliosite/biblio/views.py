from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ListBooks
from .forms import FindBook

# Create your views here.
class ListBooksPage(ListView):
    '''Displays a list of all books or books found by the specified title.'''
    model = ListBooks
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            self.form = FindBook(self.request.GET)
        else:
            self.form = FindBook()
        context['form'] = self.form
        context['find_title'] = self.request.GET.get('title', 0)
        context['find_author'] = self.request.GET.get('author', 0)
        return context


class DetailBook(DetailView):
    '''Show full information about the book.'''
    model = ListBooks