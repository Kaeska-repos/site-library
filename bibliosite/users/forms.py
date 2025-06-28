from django import forms
from django.contrib.auth.models import Group, User
from django.core.validators import RegexValidator
from datetime import date


class UserChoice(forms.ModelChoiceField):
    '''Display the users first and last name in the drop-down list.'''
    def label_from_instance(self, obj):
        return f'{obj.last_name} {obj.first_name}'


# Forms.
class RegisterForm(forms.ModelForm):
    '''The basic user registration form.'''
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


class RegisterUserForm(RegisterForm):
    '''Employee registration form.'''
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), label='Должность')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')
    btn_label = [('register', 'Зарегистрировать'),]
 
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'groups', 'email', 'password', 'password2']
        labels = {
            'username': 'Логин',
            'email': 'E-mail',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    

class RegisterReaderForm(RegisterForm):
    '''A form for registering readers.'''
    current_year = date.today().year
    btn_label = [('register', 'Зарегистрировать'),]

    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')
    phone = forms.IntegerField(validators=[RegexValidator(regex=r'^\d{10}$')], label='Телефон')
    date_birth = forms.DateField(
        label='Дата рождения', 
        widget=forms.SelectDateWidget(years=range(current_year - 120, current_year - 13)), initial=date(year=(current_year - 14), month=1, day=1)
    )

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'date_birth', 'phone', 'email', 'password', 'password2']
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    

class EditUserForm(forms.ModelForm):
    '''Employee edit form.'''
    btn_disabled = False
    btn_label = [('edit', 'Изменить'), ('delete', 'Удалить')]

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']
        labels = {
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Такой email уже существует.')
        return email


class EditReaderForm(forms.ModelForm):
    '''Reader edit form.'''
    phone = forms.IntegerField(validators=[RegexValidator(regex=r'^\d{10}$')], label='Телефон')
    btn_disabled = False
    btn_label = [('edit', 'Изменить'), ('delete', 'Удалить')]

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'phone', 'email']
        labels = {
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Такой email уже существует.')
        return email


class SelectUserForm(forms.Form):
    '''Find an employee.'''
    list_person = UserChoice(
        queryset=User.objects.filter(is_superuser=0, groups__name__isnull=False).order_by('last_name'), 
        label='Зарегистрированые'
    )
    btn_label = [('select', 'Выбрать'),]


class SelectReaderForm(forms.Form):
    '''Find an reader.'''
    list_person = UserChoice(
        queryset=User.objects.filter(is_superuser=0, groups__name__isnull=True).order_by('last_name'), 
        label='Зарегистрированые'
    )
    btn_label = [('select', 'Выбрать'),]