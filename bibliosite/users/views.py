from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from datetime import date
from django.http import HttpResponse

from .forms import *
from .models import Readers

# Create your views here.
class LoginUser(LoginView):
    '''Authorization.'''
    form_class = AuthenticationForm
    template_name = 'users\login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
@permission_required(perm='auth.add_user', raise_exception=True)
def register(request):
    '''Employee registration.'''
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.groups.add(request.POST['groups'])
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})


@permission_required(perm='users.add_readers', raise_exception=True)
def reg_reader(request):
    '''Register readers.'''
    if request.method == "POST":
        form = RegisterReaderForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            birth = date(year=int(request.POST['date_birth_year']), month=int(request.POST['date_birth_month']), day=int(request.POST['date_birth_day']))
            add_info_user = Readers(phone=request.POST['phone'], date_birth=birth, user_id=user.id)
            add_info_user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterReaderForm()
    return render(request, 'users/register_reader.html', {'form': form})