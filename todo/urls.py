from django.urls import path
from .views import MainList, Detail, CreateTask, UpdateTask, DeleteTask

urlpatterns = [
    path("", MainList.as_view() , name="tasks"),
    path("task/<int:pk>/", Detail.as_view(), name="detail"),
    path("create", CreateTask.as_view() , name="create"),
    path("edit/<int:pk>/", UpdateTask.as_view() , name="edit"),
    path("delete/<int:pk>/", DeleteTask.as_view() , name="delete"),
]