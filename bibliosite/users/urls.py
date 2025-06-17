from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from . import views

app_name = "users"
 
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', PasswordResetView.as_view(template_name="one_form.html", email_template_name="users/password_reset_email.html", success_url=reverse_lazy("users:password_reset_done"), extra_context={'title': 'Восстановление пароля', 'label_button': 'Сбросить по E-mail', 'not_title_authorization': False}), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="just_a_line.html", extra_context={'text': 'Пароль был отправлен на электронную почту.', 'not_title_authorization': True}), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="one_form.html", success_url=reverse_lazy("users:password_reset_complete"), extra_context={'title': 'Введите новый пароль', 'label_button': 'Сохранить', 'not_title_authorization': True}), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="just_a_line.html", extra_context={'text': 'Пароль был изменён.', 'title_not_authorization': False}), name='password_reset_complete'),
    path('register/reader/', views.reg_reader, name='reg_reader'),
]