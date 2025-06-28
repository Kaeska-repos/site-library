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
        context['title'] = self.request.GET.get('title', '')
        context['author'] = self.request.GET.get('author', '')
        return context
    
    def get_queryset(self):
        if self.request.GET.get('title', ''):
            find_book = ListBooks.objects.filter(title__icontains=self.request.GET.get('title', ''), author__icontains=self.request.GET.get('author', ''))
        else:
            find_book = super().get_queryset()
        return find_book


class DetailBook(DetailView):
    '''Show full information about the book.'''
    model = ListBooks

    def get_context_data(self, **kwargs):
        count = Distribution.objects.filter(book_id=kwargs['object'].id).count()
        count = kwargs['object'].numberofbooks.number - count
        context = super().get_context_data(**kwargs)
        context['number_of_books'] = count
        context['form_edit'] = NumberOfBooksForm(initial={
            'number': kwargs['object'].numberofbooks.number,
            'additionally': kwargs['object'].numberofbooks.additionally
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        if request.POST['form_button'] == 'edit':
            edit_book = NumberOfBooks.objects.get(book=kwargs['pk'])
            edit_book.number = request.POST['number']
            edit_book.additionally = request.POST['additionally']
            edit_book.save()
        else:
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
        book = form.save()
        number_of_books = NumberOfBooks(number=self.request.POST['number'], additionally=self.request.POST['additionally'], book_id=book.id)
        number_of_books.save()
        return super().form_valid(form)


def register_distribution(request):
    if request.method == "POST":
        if request.POST['form_button'] == 'select':
            # Action after selecting an already registered reader from the list.
            form_register = DistributionForm()
            form_select = DistributionSelect(request.POST)
            person_id = request.POST['field']
            form_delete = DistributionDelete(person_id=person_id)
            request.session['usi'] = person_id
            message = ''
        elif request.POST['form_button'] == 'delete':
            # Deleting distribution data.
            form_register = DistributionForm()
            form_select = DistributionSelect(initial={'field': request.session['usi']})
            Distribution.objects.get(id=request.POST['book']).delete()
            form_delete = DistributionDelete(person_id=request.session['usi'])
            message = 'Данные были удалены.'
        else:
            # Saving data about a new reader in the database.
            form_delete = DistributionDelete()
            form_select = DistributionSelect()
            form_register = DistributionForm(request.POST)
            if form_register.is_valid():
                form_register.save()
                message = 'Регистрация прошла успешно.'
            else:
                message = 'Некорректно введены данные!'
            request.session['usi'] = None
    else:
        form_register = DistributionForm()
        form_delete = DistributionDelete()
        form_select = DistributionSelect()
        message = ''
        request.session['usi'] = None
    if request.session['usi'] is None:
        DistributionDelete.btn_disabled = True
    else:
        DistributionDelete.btn_disabled = False
    return render(request, 'three_forms.html', 
                  {
                      'form_register': form_register, 
                      'form_edit': form_delete, 
                      'form_select': form_select, 
                      'title_left': 'Выдача книг', 
                      'title_right': 'Удаление данных о выдаче', 
                      'message': message,
                  }
    )