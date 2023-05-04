from django.db import models
from django.contrib.auth.models import User
import uuid

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quiz_ID = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    taker_name = models.CharField(max_length=255)
    score = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)