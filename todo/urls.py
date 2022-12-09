from django.urls import path
from .views import MainList, CreateTask, UpdateTask, DeleteTask

urlpatterns = [
    path("", MainList.as_view() , name="todo"),
    path("create", CreateTask.as_view() , name="create"),
    path("edit/<int:pk>/", UpdateTask.as_view() , name="edit"),
    path("delete/<int:pk>/", DeleteTask.as_view() , name="delete"),
]