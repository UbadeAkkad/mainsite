from django.contrib import admin
from .models import Note

# Register your models here.

admin.site.register(Note, list_display = ["title","user","created"])