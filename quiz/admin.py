from django.contrib import admin
from .models import Quiz, Question, Answer, Result

admin.site.register(Quiz, list_display = ["name", "quiz_ID", "created","user"])
admin.site.register(Question, list_display = ["text", "quiz"])
admin.site.register(Answer, list_display = ["text", "is_correct","question"])
admin.site.register(Result, list_display = ["taker_name", "created","score", "quiz"])