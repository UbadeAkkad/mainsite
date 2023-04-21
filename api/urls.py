from .views import RegisterAPI, LoginAPI, LogoutAPI, GuestLoginAPI, ConvertGuestToUser, NotesAPI, TasksAPI
from django.urls import path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from .schemas import CustomMainSchema

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('guestlogin', GuestLoginAPI.as_view()),
    path('convertguest', ConvertGuestToUser.as_view()),
    path('notes', NotesAPI.as_view()),
    path('tasks', TasksAPI.as_view()),
    path('openapi', get_schema_view(
        title="REST API",
        description="API documentation.",
        version="1.0.0",
        generator_class=CustomMainSchema,
        urlconf='api.urls',
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]