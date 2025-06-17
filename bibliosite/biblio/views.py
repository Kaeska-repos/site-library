from django import http
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render

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

    def post(self, request, *args, **kwargs):
        ListBooks.objects.get(pk=kwargs['pk']).delete()
        return http.HttpResponse("Книга удалена.")


class RegisterBooks(PermissionRequiredMixin, FormView):
    '''Book registration in the database.'''
    form_class = RegisterBook
    template_name = 'one_form.html'
    success_url = reverse_lazy('home')
    permission_required = 'biblio.add_listbooks'

    extra_context = {
        'title': 'Регистрация книг',
        'label_button': 'Зарегистрировать',
        'not_title_authorization': False,
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

user_id = None


def register_distribution(request):
    global user_id
    if request.method == "POST":
        if request.POST['check'] == 'select':
            # Action after selecting an already registered reader from the list.
            form_register = DistributionForm()
            form_select = DistributionSelect(request.POST)
            person_id = request.POST['field']
            form_delete = DistributionDelete(person_id=person_id)
            user_id = person_id
        elif request.POST['check'] == 'edit':
            # Deleting distribution data.
            form_register = DistributionForm()
            form_select = DistributionSelect(initial={'field': user_id})
            Distribution.objects.get(id=request.POST['book']).delete()
            form_delete = DistributionDelete(person_id=user_id)
        else:
            # Saving data about a new reader in the database.
            form_delete = DistributionDelete()
            form_select = DistributionSelect()
            form_register = DistributionForm(request.POST)
            if form_register.is_valid():
                form_register.save()
            user_id = None
    else:
        form_register = DistributionForm()
        form_delete = DistributionDelete()
        form_select = DistributionSelect()
        user_id = None
    return render(request, 'three_forms.html', {'form_register': form_register, 'form_edit': form_delete, 'form_select': form_select, 'title_left': 'Выдача книг', 'title_right': 'Удаление данных о выдаче', 'user_id': user_id})