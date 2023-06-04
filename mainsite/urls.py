from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('notadmin/', admin.site.urls),   # :D
    path('', include("home.urls")),
    re_path(r'^webpush/', include('webpush.urls')),
]
