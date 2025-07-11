from django.urls import path

from . import views
 
urlpatterns = [
    path('', views.ListBooksPage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('<pk>/', views.DetailBook.as_view(), name='detail'),
    path('register/book', views.RegisterBooks.as_view(), name='reg_book'),
    path('register/distribution/', views.register_distribution, name='reg_distribution'),
]