from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')
 
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2', 'groups']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
            'email': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }
        

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже существует.')
        return email