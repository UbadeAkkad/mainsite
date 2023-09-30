from django.contrib import admin
from .models import Message, Question


admin.site.register(Message, list_display = ["created","author"])
admin.site.register(Question, list_display = ["created","author","question_ID"])