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
    form_class.btn_label = [('auth', 'Войти'),]
    template_name = 'users\login.html'

    extra_context = {
        'title': 'Авторизация',
        'label_button': 'Войти',
        'not_title_authorization': True,
    }

    def get_success_url(self):
        return reverse_lazy('home')


user_id = None


@permission_required(perm='auth.add_user', raise_exception=True)
def register(request):
    '''Employee registration. As well as changing data about already registered employees.'''
    global user_id
    if request.method == "POST":
        if request.POST['form_button'] == 'register':
            # Saving data about a new employee in the database.
            user_id = None
            form_select = SelectUserForm()
            form_edit = EditUserForm()
            form_register = RegisterUserForm(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.set_password(form_register.cleaned_data['password'])
                user.save()
                user.groups.add(request.POST['groups'])
                message = 'Регистрация прошла успешно.'
            else:
                message = 'Некорректно введены данные!'
        elif request.POST['form_button'] == 'select':
            # Action after selecting an already registered employee from the list.
            form_register = RegisterUserForm()
            form_select = SelectUserForm()
            user_id = request.POST['list_employee']
            employee_list = list(User.objects.filter(id=user_id).values('last_name', 'first_name', 'email'))
            employee_query = QueryDict("", mutable=True)
            employee_query.update(employee_list[0])
            form_edit = EditUserForm(employee_query, instance=User.objects.get(id=user_id))
            message = ''
        else:
            # Saving the changed employee data in the database.
            form_register = RegisterUserForm()
            form_select = SelectUserForm()
            if request.POST['form_button'] == 'edit':
                form_edit = EditUserForm(request.POST, instance=User.objects.get(id=user_id))
                if form_edit.is_valid():
                    form_edit.save()  # Saving changes to employee data.
                    message = 'Изменения успешно внесены в базу данных.'
                else:
                    message = 'Некорректно введены данные!'
            elif request.POST['form_button'] == 'delete':
                # Deleting employee data.
                User.objects.get(id=user_id).delete()
                user_id = None
                message = 'Данные о сотруднике были удалены.'
                form_edit = EditUserForm()
    else:
        form_register = RegisterUserForm()
        form_edit = EditUserForm()
        form_select = SelectUserForm()
        user_id = None
        message = ''
    if user_id is None:
        EditUserForm.btn_disabled = True
    else:
        EditUserForm.btn_disabled = False
    return render(request, 'three_forms.html',
                  {
                      'form_register': form_register, 
                      'form_edit': form_edit, 
                      'form_select': form_select, 
                      'title_left': 'Регистрация сотрудников', 
                      'title_right': 'Информация о сотрудниках',
                      'message': message,
                  }
    )


@permission_required(perm='users.add_readers', raise_exception=True)
def reg_reader(request):
    '''Register readers.'''
    global user_id
    if request.method == "POST":
        if request.POST['form_button'] == 'register':
            # Saving data about a new reader in the database.
            user_id = None
            form_edit = EditReaderForm()
            form_select = SelectReaderForm()
            form_register = RegisterReaderForm(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.set_password(form_register.cleaned_data['password'])
                user.save()
                birth = date(year=int(request.POST['date_birth_year']), month=int(request.POST['date_birth_month']), day=int(request.POST['date_birth_day']))
                add_info_user = Readers(phone=request.POST['phone'], date_birth=birth, user_id=user.id)
                add_info_user.save()
                message = 'Регистрация прошла успешно.'
            else:
                message = 'Некорректно введены данные!'
        elif request.POST['form_button'] == 'select':
            # Action after selecting an already registered reader from the list.
            form_register = RegisterReaderForm()
            form_select = SelectReaderForm()
            user_id = request.POST['list_readers']
            reader_list = list(User.objects.filter(id=user_id).values('last_name', 'first_name', 'email'))
            reader_list[0]['phone'] = User.objects.get(id=user_id).readers.phone
            reader_query = QueryDict("", mutable=True)
            reader_query.update(reader_list[0])
            form_edit = EditReaderForm(reader_query, instance=User.objects.get(id=user_id))
            message = ''
        else:
            # Saving the changed reader data in the database.
            form_register = RegisterReaderForm()
            form_select = SelectReaderForm()
            if request.POST['form_button'] == 'edit':
                # Saving changes to reader data.
                form_edit = EditReaderForm(request.POST, instance=User.objects.get(id=user_id))
                if form_edit.is_valid():
                    form_edit.save()
                    user_phone = User.objects.get(id=user_id).readers
                    user_phone.phone = request.POST['phone']
                    user_phone.save()
                    message = 'Изменения успешно внесены в базу данных.'
                else:
                    message = 'Некорректно введены данные!'
            elif request.POST['form_button'] == 'delete':
                # Deleting reader data.
                User.objects.get(id=user_id).delete()
                user_id = None
                message = 'Данные о сотруднике были удалены.'
                form_edit = EditReaderForm()
    else:
        form_register = RegisterReaderForm()
        form_edit = EditReaderForm()
        form_select = SelectReaderForm()
        user_id = None
        message = ''
    if user_id is None:
        EditUserForm.btn_disabled = True
    else:
        EditUserForm.btn_disabled = False
    return render(request, 'three_forms.html',
                  {
                      'form_register': form_register, 
                      'form_edit': form_edit, 
                      'form_select': form_select, 
                      'title_left': 'Регистрация читателей', 
                      'title_right': 'Информация о читателях',
                      'message': message,
                  }
    )