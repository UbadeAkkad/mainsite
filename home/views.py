from django.views.generic import TemplateView, FormView, CreateView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404, render
from guest_user.decorators import allow_guest_user
from .models import Message, Question
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git
import requests
from decouple import config

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
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            ["Todo List App","todo","Simple todo list app."],
            ["Notes App","notes","Simple notes app."],
            ["Quiz App","quiz_list","Create and share quizzes."],
            ["REST APIs","swagger-ui","Swagger API Documentation."],
            #["React App","reactapp","A React app that uses the REST APIs   #Still working on it!"],
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
        if self.request.POST.get("question") == "on":
            if self.request.user.is_authenticated:
                added_question = Question.objects.create(author=self.request.user.get_username(),
                                        question=self.request.POST.get("message"))
            else:
                added_question = Question.objects.create(author="Anonymous",
                                        question=self.request.POST.get("message"))
            return redirect(reverse('question_created', kwargs={ 'id': str(added_question.question_ID) }))
        else:
            if self.request.user.is_authenticated:
                form.instance.author = self.request.user.get_username()
            else:
                form.instance.author = "Anonymous"
            return super(AddMessage, self).form_valid(form)

class QuestionPage(View):
    def get(self, request, id):
        question = get_object_or_404(Question, question_ID=id)
        return render(request, 'home/question_page.html', {"question": question.question, "answer": question.answer})

def Pythonanywhere_update():
    username = 'Ubade'
    token = config("PYTHONANYWHERE_TOKEN")
    domain_name = "ubade.pythonanywhere.com"

    response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username=username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)

    return str(response.status_code)

@csrf_exempt
def Git_Pull(request):
    if request.method == "POST":
        repo = git.Repo("") 
        origin = repo.remotes.origin
        origin.pull()
        Web_reload = Pythonanywhere_update()
        return HttpResponse("Updated the code, and Web reload code: " + Web_reload)
    else:
        return HttpResponse("Couldn't update the code!")