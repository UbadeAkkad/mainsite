from django.db import models
import uuid

class Message(models.Model):
    author = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.created)
    
class Question(models.Model):
    author = models.CharField(max_length=200)
    question = models.TextField()
    answer = models.TextField(default="", blank=True)
    question_ID = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.created)
