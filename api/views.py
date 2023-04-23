from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, GuestUserSerializer, NoteSerializer, TaskSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from notes.models import Note
from todo.models import Task
import json
from django.shortcuts import get_object_or_404
from .schemas import RegisterSchema, LoginSchema, LogoutSchema, GuestLoginSchema, ConvertGuestSchema, NoteSchema, TaskSchema
from guest_user.functions import maybe_create_guest_user
from guest_user.models import Guest

class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    schema = RegisterSchema()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "username": UserSerializer(user, context=self.get_serializer_context()).data["username"],
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView, GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    schema = LoginSchema()

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super(LoginAPI, self).post(request, format=None)
        response.data["username"] = UserSerializer(user, context=self.get_serializer_context()).data["username"]
        return response

class LogoutAPI(KnoxLogoutView):
    permission_classes = (AllowAny,)
    schema = LogoutSchema()

class GuestLoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)
    schema = GuestLoginSchema()

    def post(self, request, format=None):
        maybe_create_guest_user(request)
        return super(GuestLoginAPI, self).post(request, format=None)

class ConvertGuestToUser(GenericAPIView):
    serializer_class = GuestUserSerializer
    schema = ConvertGuestSchema()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()    #update the guest user with the new username and password
            updated_user.set_password(serializer.data.get('password'))
            updated_user.save()
            Guest.objects.filter(user=request.user).delete()  #remove the user record from the Guest model
            return Response(UserSerializer(updated_user, context=self.get_serializer_context()).data, status=200)
        else:
            return Response("Data Error!", status=400)

#Note App
class NotesAPI(GenericAPIView):
    serializer_class = NoteSerializer
    schema = NoteSchema()

    def get(self,request):
        if request.user.is_authenticated:
            items = Note.objects.filter(user=request.user).order_by('-created')
            id_parameter = request.query_params.get('id') or ''
            if id_parameter :
                items = items.filter(id=id_parameter)
                if len(items) == 0:
                    return Response("Note not found!", status=404)
            seri = NoteSerializer(items, many=True)
            return Response(seri.data)
        else:
            return Response("Not authorized!", status=401)

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
                return Response("Request body Error!", status=400)
            return Response("Note added", status=200)
        else:
            return Response("Not authorized!", status=401)

    def delete(self,request):
        if request.user.is_authenticated:
            items = Note.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                note = get_object_or_404(items, id=body["id"])
                note.delete()
            except:
                return Response("ID Error!", status=400)
            return Response("Note deleted", status=200)
        else:
            return Response("Not authorized!", status=401)

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
                return Response("Request body Error!", status=400)
            return Response("Note updated", status=200)
        else:
            return Response("Not authorized!", status=401)


#Todo App
class TasksAPI(GenericAPIView):
    serializer_class = TaskSerializer
    schema = TaskSchema()

    def get(self,request):
        if request.user.is_authenticated:
            items = Task.objects.filter(user=request.user).order_by('-created')
            id_parameter = request.query_params.get('id') or ''
            if id_parameter :
                items = items.filter(id=id_parameter)
                if len(items) == 0:
                    return Response("Task not found!", status=404)
            seri = TaskSerializer(items, many=True)
            return Response(seri.data)
        else:
            return Response("Not authorized!", status=401)

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
                return Response("Request body Error!", status=400)
            return Response("Task added", status=200)
        else:
            return Response("Not authorized!", status=401)

    def delete(self,request):
        if request.user.is_authenticated:
            items = Task.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                task = get_object_or_404(items, id=body["id"])
                task.delete()
            except:
                return Response("ID Error!", status=400)
            return Response("Task deleted", status=200)
        else:
            return Response("Not authorized!", status=401)

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
                return Response("Request body Error!", status=400)
            return Response("Task updated", status=200)
        else:
            return Response("Not authorized!", status=401)