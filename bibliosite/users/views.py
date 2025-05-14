from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from bibliosite import settings
from .forms import RegisterUserForm

# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users\login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    

def register(request):
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