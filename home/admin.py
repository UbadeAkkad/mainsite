from django.contrib import admin
from .models import Message


admin.site.register(Message, list_display = ["created","author"])