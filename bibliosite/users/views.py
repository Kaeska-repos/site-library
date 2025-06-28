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


def register_all(request, f_edit, f_register, f_select, t_left, t_right, add_phone=False):
    '''Registration of people. As well as changing data about already registered people.'''
    if request.method == "POST":
        # Saving data about a new person in the database.
        if request.POST['form_button'] == 'register':
            request.session['usi'] = None
            form_select = f_select()
            form_edit = f_edit()
            form_register = f_register(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.set_password(form_register.cleaned_data['password'])
                user.save()
                if add_phone:
                    birth = date(year=int(request.POST['date_birth_year']), month=int(request.POST['date_birth_month']), day=int(request.POST['date_birth_day']))
                    add_info_user = Readers(phone=request.POST['phone'], date_birth=birth, user_id=user.id)
                    add_info_user.save()
                else:
                    user.groups.add(request.POST['groups'])
                message = 'Регистрация прошла успешно.'
            else:
                message = 'Некорректно введены данные!'
        elif request.POST['form_button'] == 'select':
            # Action after selecting an already registered person from the list.
            form_register = f_register()
            form_select = f_select()
            request.session['usi'] = request.POST['list_person']
            employee_list = list(User.objects.filter(id=request.session['usi']).values('last_name', 'first_name', 'email'))
            if add_phone:
                employee_list[0]['phone'] = User.objects.get(id=request.session['usi']).readers.phone
            employee_query = QueryDict("", mutable=True)
            employee_query.update(employee_list[0])
            form_edit = f_edit(employee_query, instance=User.objects.get(id=request.session['usi']))
            message = ''
        else:
            # Saving the changed person data in the database.
            form_register = f_register()
            form_select = f_select()
            if request.POST['form_button'] == 'edit':
                form_edit = f_edit(request.POST, instance=User.objects.get(id=request.session['usi']))
                if form_edit.is_valid():
                    form_edit.save() # Saving changes to person data.
                    if add_phone:
                        user_phone = User.objects.get(id=request.session['usi']).readers
                        user_phone.phone = request.POST['phone']
                        user_phone.save()
                    message = 'Изменения успешно внесены в базу данных.'
                else:
                    message = 'Некорректно введены данные!'
            elif request.POST['form_button'] == 'delete':
                # Deleting person data.
                User.objects.get(id=request.session['usi']).delete()
                request.session['usi'] = None
                message = 'Данные о сотруднике были удалены.'
                form_edit = f_edit()
    else:
        form_register = f_register()
        form_edit = f_edit()
        form_select = f_select()
        request.session['usi'] = None
        message = ''
    if request.session['usi'] is None:
        f_edit.btn_disabled = True
    else:
        f_edit.btn_disabled = False
    return render(request, 'three_forms.html',
                  {
                      'form_register': form_register, 
                      'form_edit': form_edit, 
                      'form_select': form_select, 
                      'title_left': t_left, 
                      'title_right': t_right,
                      'message': message,
                  }
    )


@permission_required(perm='auth.add_user', raise_exception=True)
def register(request):
    '''Employee registration. As well as changing data about already registered employees.'''
    return register_all(
        request, 
        EditUserForm, 
        RegisterUserForm, 
        SelectUserForm, 
        'Регистрация сотрудников', 
        'Информация о сотрудниках'
    )


@permission_required(perm='users.add_readers', raise_exception=True)
def reg_reader(request):
    '''Register readers.'''
    return register_all(
        request, 
        EditReaderForm, 
        RegisterReaderForm, 
        SelectReaderForm, 
        'Регистрация читателей', 
        'Информация о читателях', 
        add_phone=True
    )