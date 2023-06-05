from django.urls import path, include, re_path
from .views import LoginPage, Register, Homepage, GuestLogin, AddMessage, Git_Pull
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path("login", LoginPage.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page='/'), name="logout"),
    path("register", Register.as_view(), name="register"),
    path("", Homepage.as_view() , name="home"),
    path("accounts/profile/",lambda request: redirect('home', permanent=False)),
    path('todo/', include("todo.urls")),
    path('notes/', include("notes.urls")),
    path("convert", include("guest_user.urls")),
    path("guestlogin", GuestLogin, name="guestlogin"),
    path("message", AddMessage.as_view(), name="leaveamessage"),
    path('api/', include("api.urls")),
    path('react', include("react_app.urls")),
    path("git_pull/", Git_Pull, name="gitpull"),
    path("github", lambda request: redirect("https://github.com/UbadeAkkad", permanent=False), name="githubaccount"),
    path("linkedin", lambda request: redirect("https://www.linkedin.com/in/ubade-akkad/", permanent=False), name="linkedinaccount"),
    path("robots.txt",TemplateView.as_view(template_name="home/robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('storage/', include("storage.urls")),
    path('quiz/', include("quiz.urls")),
    re_path(r'^webpush/', include('webpush.urls')),
]