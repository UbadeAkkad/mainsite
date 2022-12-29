from .views import RegisterAPI, LoginAPI, GetNotesAPI, AddNoteAPI, DeleteNoteAPI, UpdateNoteAPI, GetTasksAPI, AddTaskAPI, DeleteTaskAPI, UpdateTaskAPI
from django.urls import path
from knox import views as knox_views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from .schemas import CustomMainSchema

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', knox_views.LogoutView.as_view()),
    path('notes', GetNotesAPI.as_view()),
    path('notes/add', AddNoteAPI.as_view()),
    path('notes/delete', DeleteNoteAPI.as_view()),
    path('notes/update', UpdateNoteAPI.as_view()),
    path('tasks', GetTasksAPI.as_view()),
    path('tasks/add', AddTaskAPI.as_view()),
    path('tasks/delete', DeleteTaskAPI.as_view()),
    path('tasks/update', UpdateTaskAPI.as_view()),
    path('openapi', get_schema_view(
        title="REST API",
        description="API for the project apps.",
        version="1.0.0",
        generator_class=CustomMainSchema,
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]