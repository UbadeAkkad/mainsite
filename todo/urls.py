from django.urls import path
from .views import MainList, CreateTask, UpdateTask, DeleteTask, export_file

urlpatterns = [
    path("", MainList.as_view() , name="todo"),
    path("create", CreateTask.as_view() , name="createtask"),
    path("edit/<int:pk>/", UpdateTask.as_view() , name="edittask"),
    path("delete/<int:pk>/", DeleteTask.as_view() , name="deletetask"),
    path("exporttasks", export_file , name="exporttasks"),
    path("completecheck/<int:pk>/", MainList.as_view() , name="completecheck"),
]