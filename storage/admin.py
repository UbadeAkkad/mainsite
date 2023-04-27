from django.contrib import admin
from .models import UploadedFile
import os

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'download_link', 'uploaded_at')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if os.path.isfile(obj.file.path):
                os.remove(obj.file.path)
        super().delete_queryset(request, queryset)

admin.site.register(UploadedFile, UploadedFileAdmin)