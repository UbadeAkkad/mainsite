from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task    
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import PermissionDenied

class MainList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['tasks'] = context['tasks'].order_by('-created')
        search_input = self.request.GET.get('search_query') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description']
    success_url = reverse_lazy("todo")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)
    
class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'todo/task_update.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy("todo")

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo")

def export_file(request):
    if not request.user.is_authenticated:
        raise  PermissionDenied()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    content = Task.objects.filter(user=request.user).order_by('-created').values()
    worksheet.write(0, 0, "Title")
    worksheet.write(0, 1, "Description")
    worksheet.write(0, 2, "Status")
    i = 1
    for item in content:
        worksheet.write(i, 0, item["title"])
        worksheet.write(i, 1, item["description"])
        status =""
        if (item["complete"]):
             status = "Completed"
        else:
            status = "Incompleted"
        worksheet.write(i, 2, status)
        i += 1
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = request.user.username + "'s Tasks_" +datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    response['Content-Disposition'] = 'attachment;filename=' + filename + '.xlsx'
    response.write(output.getvalue())
    return response
