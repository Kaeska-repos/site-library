from django.contrib import admin
from django.db import models
from datetime import date

from .models import ListBooks, Readers, Distribution
from bibliosite.widgets import Calendar

# Register your models here.
admin.site.site_header = "Администрирование библиотеки"

@admin.register(ListBooks)
class ListBooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_per_page = 10

@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': Calendar(attrs={'value': date.today()})}
    }

@admin.register(Readers)
class ReadersAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': Calendar(attrs={'value': date(year=2000, month=1, day=1)})}
    }