from django.db import models

class Message(models.Model):
    author = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.created