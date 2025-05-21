from django import http
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import ListBooks
from .forms import *

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


class RegisterBooks(PermissionRequiredMixin, FormView):
    '''Book registration in the database.'''
    form_class = RegisterBook
    template_name = 'biblio/register_book.html'
    success_url = reverse_lazy('home')
    permission_required = 'biblio.add_listbooks'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegisterDistribution(FormView):
    '''Registration of giving the book to the reader.'''
    form_class = DistributionForm
    template_name = 'biblio/reg_distribution.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)