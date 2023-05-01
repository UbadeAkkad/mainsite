from django.contrib import admin
from .models import Quiz, Question, Answer

admin.site.register(Quiz, list_display = ["name", "quiz_ID","user"])
admin.site.register(Question, list_display = ["text", "quiz"])
admin.site.register(Answer, list_display = ["text", "is_correct","question"])