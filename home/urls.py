from django.urls import path, include
from .views import LoginPage, Register, Homepage, GuestLogin, AddMessage
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("", Homepage.as_view() , name="home"),
    path("accounts/profile/",lambda request: redirect('home', permanent=False)),
    path('todo/', include("todo.urls")),
    path('notes/', include("notes.urls")),
    path("convert/", include("guest_user.urls")),
    path("guestlogin", GuestLogin, name="guestlogin"),
    path("message", AddMessage.as_view(), name="leaveamessage"),
    path('api/', include("api.urls")),
    path('react', include("react_app.urls")),
]