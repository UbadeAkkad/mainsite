from django.urls import path
from .views import NoteList, CreateNote, UpdateNote, DeleteNote

urlpatterns = [
    path("", NoteList.as_view() , name="notes"),
    path("create", CreateNote.as_view() , name="createnote"),
    path("edit/<int:pk>/", UpdateNote.as_view() , name="editnote"),
    path("delete/<int:pk>/", DeleteNote.as_view() , name="deletenote"),
]