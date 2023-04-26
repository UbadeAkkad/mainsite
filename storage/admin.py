from django.contrib import admin
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'download_link', 'uploaded_at')

admin.site.register(UploadedFile, UploadedFileAdmin)