from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Note    
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from guest_user.functions import is_guest_user
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class NoteList(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = "notes"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['notes'] = context['notes'].order_by('-created')
        return context

    def post(self, request):
        pk = request.POST["pk"]
        color = request.POST["color"]
        changednote = get_object_or_404(Note, id=pk)
        if (color == "#ffffff" or color == "#212529"):
            color = "default"
        changednote.color = color
        changednote.save()
        return HttpResponse()

class CreateNote(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/note_create.html'
    fields = ['title','body']
    success_url = reverse_lazy("notes")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateNote, self).form_valid(form)
    
class UpdateNote(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/note_update.html'
    fields = ['title','body']
    success_url = reverse_lazy("notes")

    def form_valid(self, form):
        form.instance.created = datetime.now()
        return super(UpdateNote, self).form_valid(form)

class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'
    context_object_name = "note"
    success_url = reverse_lazy("notes")

def export_file(request):
    if not request.user.is_authenticated:
        raise  PermissionDenied()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    content = Note.objects.filter(user=request.user).order_by('-created').values()
    worksheet.write(0, 0, "Title")
    worksheet.write(0, 1, "Note")
    i = 1
    for item in content:
        worksheet.write(i, 0, item["title"])
        worksheet.write(i, 1, item["body"])
        i += 1
    workbook.close()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if is_guest_user(request.user):
        filename = "Guest's Notes_" +datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    else:
        filename = request.user.username + "'s Notes_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    response['Content-Disposition'] = 'attachment;filename=' + filename + '.xlsx'
    response.write(output.getvalue())
    return response
