from django.contrib import admin
from .models import ListBooks

# Register your models here.
admin.site.site_header = "Администрирование библиотеки"

@admin.register(ListBooks)
class ListBooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_per_page = 10