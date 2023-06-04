from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('notadmin/', admin.site.urls),   # :D
    path('', include("home.urls")),
]
