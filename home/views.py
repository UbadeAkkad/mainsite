from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from guest_user.decorators import allow_guest_user

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
        ]
        return context

@allow_guest_user
def GuestLogin(request):
    return redirect('home')