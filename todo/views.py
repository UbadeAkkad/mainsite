from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Task    
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class MainList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search_input = self.request.GET.get('search_query') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context

class Detail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description']
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)
    
class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description']
    success_url = reverse_lazy("tasks")

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
