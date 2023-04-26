from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import UploadedFile

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, download_ID=file_id)
    file = uploaded_file.file.path
    response = FileResponse(open(file, 'rb'))
    return response