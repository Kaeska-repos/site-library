from django.urls import path

from . import views
 
urlpatterns = [
    path('', views.ListBooksPage.as_view(), name='home'),
    path('<pk>/', views.DetailBook.as_view(), name='detail'),
]