from datetime import date
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import QueryDict

from .forms import *
from .models import *


# Create your views here.
class LoginUser(LoginView):
    '''Authorization.'''
    form_class = AuthenticationForm
    template_name = 'users\login.html'

    def get_success_url(self):
        return reverse_lazy('home')


user_id = None


@permission_required(perm='auth.add_user', raise_exception=True)
def register(request):
    '''Employee registration. As well as changing data about already registered employees.'''
    global user_id
    if request.method == "POST":
        if request.POST['check'] == 'select':
            # Action after selecting an already registered employee from the list.
            form_register = RegisterUserForm()
            form_select = SelectUserForm(request.POST)
            user_id = request.POST['list_employee']
            employee_list = list(User.objects.filter(id=user_id).values('last_name', 'first_name', 'email'))
            employee_query = QueryDict("", mutable=True)
            employee_query.update(employee_list[0])
            form_edit = EditUserForm(employee_query, instance=User.objects.get(id=user_id))
        elif request.POST['check'] == 'edit':
            # Saving the changed employee data in the database.
            form_button = request.POST.get('form_button')
            form_register = RegisterUserForm()
            form_select = SelectUserForm()
            form_edit = EditUserForm(request.POST, instance=User.objects.get(id=user_id))
            if form_button == 'edit':
                # Saving changes to employee data.
                if form_edit.is_valid():
                    form_edit.save()
                    return render(request, 'users/register_done.html')
            else:
                # Deleting employee data.
                User.objects.get(id=user_id).delete()
                form_edit = EditUserForm()
                form_register = RegisterUserForm()
                user_id = None
        else:
            # Saving data about a new employee in the database.
            form_edit = EditUserForm()
            form_select = SelectUserForm()
            form_register = RegisterUserForm(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.set_password(form_register.cleaned_data['password'])
                user.save()
                user.groups.add(request.POST['groups'])
                return render(request, 'users/register_done.html')
    else:
        form_register = RegisterUserForm()
        form_edit = EditUserForm()
        form_select = SelectUserForm()
        user_id = None
    return render(request, 'users/register.html', {'form_register': form_register, 'form_edit': form_edit, 'form_select': form_select, 'user_id': user_id})


@permission_required(perm='users.add_readers', raise_exception=True)
def reg_reader(request):
    '''Register readers.'''
    if request.method == "POST":
        form_register = RegisterReaderForm(request.POST)
        if form_register.is_valid():
            user = form_register.save(commit=False)
            user.set_password(form_register.cleaned_data['password'])
            user.save()
            birth = date(year=int(request.POST['date_birth_year']), month=int(request.POST['date_birth_month']), day=int(request.POST['date_birth_day']))
            add_info_user = Readers(phone=request.POST['phone'], date_birth=birth, user_id=user.id)
            add_info_user.save()
            return render(request, 'users/register_done.html')
    else:
        form_register = RegisterReaderForm()
    return render(request, 'users/register_reader.html', {'form_register': form_register})