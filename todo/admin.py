from django.contrib import admin
from .models import Task

# Register your models here.

admin.site.register(Task, list_display = ["title","user","complete","created"])