from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, NoteSerializer, TaskSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from django.http import HttpResponse
from notes.models import Note
from todo.models import Task
import json
from django.shortcuts import get_object_or_404
from .schemas import RegisterSchema, LoginSchema, NoteSchema, TaskSchema


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    schema = RegisterSchema()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    schema = LoginSchema()

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

#Note App
class GetNotesAPI(generics.GenericAPIView):
    serializer_class = NoteSerializer
    schema = NoteSchema()

    def get(self,request):
        if request.user.is_authenticated:
            items = Note.objects.filter(user=request.user).order_by('-created')
            seri = NoteSerializer(items, many=True)
            return Response(seri.data)
        else:
            return HttpResponse("Not authorized!")

class AddNoteAPI(generics.GenericAPIView):
    serializer_class = NoteSerializer
    schema = NoteSchema()

    def post(self,request):
        if request.user.is_authenticated:
            body = json.loads(request.body)
            note = Note()
            try:
                note.user = request.user
                note.title = body["title"]
                note.body = body["body"]
                note.save()
            except:
                return HttpResponse("Data Error!")
            return HttpResponse("Note added")
        else:
            return HttpResponse("Not authorized!")

class DeleteNoteAPI(generics.GenericAPIView):
    serializer_class = NoteSerializer
    schema = NoteSchema()

    def delete(self,request):
        if request.user.is_authenticated:
            items = Note.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                note = get_object_or_404(items, id=body["id"])
                note.delete()
            except:
                return HttpResponse("ID Error!")
            return HttpResponse("Note deleted")
        else:
            return HttpResponse("Not authorized!")

class UpdateNoteAPI(generics.GenericAPIView):
    serializer_class = NoteSerializer
    schema = NoteSchema()

    def put(self,request):
        if request.user.is_authenticated:
            items = Note.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                note = get_object_or_404(items, id=body["id"])
                if body["title"]:
                    note.title = body["title"]
                if body["body"]:
                    note.body = body["body"]
                if body["color"]:
                    note.color = body["color"]
                note.save()
            except:
                return HttpResponse("Data Error!")
            return HttpResponse("Note updated")
        else:
            return HttpResponse("Not authorized!")


#Todo App
class GetTasksAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer
    schema = TaskSchema()

    def get(self,request):
        if request.user.is_authenticated:
            items = Task.objects.filter(user=request.user).order_by('-created')
            seri = TaskSerializer(items, many=True)
            return Response(seri.data)
        else:
            return HttpResponse("Not authorized!")

class AddTaskAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer
    schema = TaskSchema()

    def post(self,request):
        if request.user.is_authenticated:
            body = json.loads(request.body)
            task = Task()
            try:
                task.user = request.user
                task.title = body["title"]
                task.description = body["description"]
                task.save()
            except:
                return HttpResponse("Data Error!")
            return HttpResponse("Task added")
        else:
            return HttpResponse("Not authorized!")

class DeleteTaskAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer
    schema = TaskSchema()

    def delete(self,request):
        if request.user.is_authenticated:
            items = Task.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                task = get_object_or_404(items, id=body["id"])
                task.delete()
            except:
                return HttpResponse("ID Error!")
            return HttpResponse("Task deleted")
        else:
            return HttpResponse("Not authorized!")

class UpdateTaskAPI(generics.GenericAPIView):
    serializer_class = TaskSerializer
    schema = TaskSchema()

    def put(self,request):
        if request.user.is_authenticated:
            items = Task.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                task = get_object_or_404(items, id=body["id"])
                if body["title"]:
                    task.title = body["title"]
                if body["description"]:
                    task.description = body["description"]
                if body["complete"] != "":
                    task.complete = body["complete"]
                task.save()
            except:
                return HttpResponse("Data Error!")
            return HttpResponse("Task updated")
        else:
            return HttpResponse("Not authorized!")