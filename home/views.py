from django.views.generic import TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from guest_user.decorators import allow_guest_user
from .models import Message  
import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class LoginPage(LoginView):
    template_name = 'home/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

class Register(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home') 
        return super(Register, self).get(*args, **kwargs)

class Homepage(TemplateView):
    template_name = 'home/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applist"] = [                          #["AppName","URL","Description"]
            ["Todo List App","todo","A simple todo list app :)"],
            ["Notes App","notes","An even simpler notes app :D"],
            ["App's REST APIs","swagger-ui","Swagger API Documentation"],
            ["React App","reactapp","A React app that uses the REST APIs   #Still working on it!"],
            ["Leave me a message","leaveamessage","It doesn't require a login!"],
        ]
        return context

@allow_guest_user
def GuestLogin(request):
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect('home')


class AddMessage(CreateView):
    model = Message
    template_name = 'home/create_message.html'
    fields = ['message']
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user.get_username()
            return super(AddMessage, self).form_valid(form)
        else:
            form.instance.author = "Anonymous"
            return super(AddMessage, self).form_valid(form)
        
@csrf_exempt
def Git_Pull(request):
    if request.method == "POST":
        repo = git.Repo("") 
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Updated the code")
    else:
        return HttpResponse("Couldn't update the code!")