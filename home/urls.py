from django.urls import path, include
from .views import LoginPage, Register, Homepage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("", Homepage.as_view() , name="home"),
    path('todo/', include("todo.urls")),
]