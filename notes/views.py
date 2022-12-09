from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Note    
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class NoteList(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = "notes"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        return context

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

class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'
    context_object_name = "note"
    success_url = reverse_lazy("notes")
