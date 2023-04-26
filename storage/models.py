from django.db import models
import uuid
import os

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255, editable=False)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_ID = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
    download_link = models.URLField(max_length=400, editable=False, default="None")

    def save(self, *args, **kwargs):
        file_name = os.path.basename(self.file.name)
        self.file_name = file_name
        self.download_link = "https://ubade.pythonanywhere.com/storage/download/" + str(self.download_ID)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.file_name