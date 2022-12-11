from django.urls import path
from .views import NoteList, CreateNote, UpdateNote, DeleteNote, export_file

urlpatterns = [
    path("", NoteList.as_view() , name="notes"),
    path("create", CreateNote.as_view() , name="createnote"),
    path("edit/<int:pk>/", UpdateNote.as_view() , name="editnote"),
    path("delete/<int:pk>/", DeleteNote.as_view() , name="deletenote"),
    path("exportnotes", export_file , name="exportnotes"),
]