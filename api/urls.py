from .views import RegisterAPI, LoginAPI, GetNotesAPI, AddNoteAPI, DeleteNoteAPI, UpdateNoteAPI, GetTasksAPI, AddTaskAPI, DeleteTaskAPI, UpdateTaskAPI
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('notes/get', GetNotesAPI),
    path('notes/add', AddNoteAPI),
    path('notes/delete', DeleteNoteAPI),
    path('notes/update', UpdateNoteAPI),
    path('tasks/get', GetTasksAPI),
    path('tasks/add', AddTaskAPI),
    path('tasks/delete', DeleteTaskAPI),
    path('tasks/update', UpdateTaskAPI),
]