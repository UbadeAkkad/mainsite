from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, GuestUserSerializer, NoteSerializer, TaskSerializer, Quizserializer, QuizPageserializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from notes.models import Note
from todo.models import Task
import json
from django.shortcuts import get_object_or_404, get_list_or_404
from .schemas import RegisterSchema, LoginSchema, LogoutSchema, GuestLoginSchema, ConvertGuestSchema, NoteSchema, TaskSchema, QuizSchema, QuizDetailsSchema, QuizPageSchema
from guest_user.functions import maybe_create_guest_user
from guest_user.models import Guest
from quiz.models import Quiz, Question, Answer, Result
from django.http import JsonResponse

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
        
#Quiz App
class QuizAPI(GenericAPIView):
    serializer_class = Quizserializer
    schema = QuizSchema()

    def get(self,request):
        if request.user.is_authenticated:
            items = Quiz.objects.filter(user=request.user).order_by('-created')
            seri = Quizserializer(items, many=True)
            return Response(seri.data)
        else:
            return Response("Not authorized!", status=401)
        
    def post(self,request):
        if request.user.is_authenticated:
            body = json.loads(request.body)
            try:
                quiz = Quiz.objects.create(user=self.request.user, name=body["name"])
                for q in body["questions"]:
                    question = Question.objects.create(quiz=quiz, text=q["question"])
                    correct_answer = q["correct_answer"]
                    answers_list = q["answers"]

                    if len(answers_list) != len(list(set(answers_list))):  #to prevent a user submitting duplicate answers for the same question.
                        quiz.delete()
                        return Response("A question can't have a duplicate answers!", status=400)
                    if correct_answer not in answers_list:      #correct answer for a question need to be from the submitted answers.
                        quiz.delete()
                        return Response("Correct answer for a question needs to be from the submitted answers!", status=400)

                    for a in answers_list:
                        Answer.objects.create(question=question, text=a, is_correct=a==correct_answer)   
            except:
                quiz.delete()
                return Response("Request body Error!", status=400)
            return Response("Quiz added", status=200)
        else:
            return Response("Not authorized!", status=401)

    def delete(self,request):
        if request.user.is_authenticated:
            quizzes = Quiz.objects.filter(user=request.user)
            body = json.loads(request.body)
            try:
                quiz = get_object_or_404(quizzes, quiz_ID=body["id"])
                quiz.delete()
            except:
                return Response("ID Error!", status=400)
            return Response("Quiz deleted", status=200)
        else:
            return Response("Not authorized!", status=401)
        
class QuizDetailsAPI(GenericAPIView):
    serializer_class = Quizserializer
    schema = QuizDetailsSchema()

    def get(self,request,quiz_id):
        if request.user.is_authenticated:
            try:
                user_quizs = Quiz.objects.filter(user=self.request.user)
                quiz = get_object_or_404(user_quizs, quiz_ID=quiz_id)
                questions = get_list_or_404(Question, quiz=quiz)
                QA = []
                for q in questions:
                    answers = []
                    for a in get_list_or_404(Answer, question=q):
                        answers.append({"answer": a.text,
                                        "correct": a.is_correct})
                    QA.append({"question": q.text,
                            "answers": answers})
                results = []
                for r in Result.objects.filter(quiz=quiz).order_by('-created'):
                    results.append({"taker_name": r.taker_name,
                                    "score": r.score,
                                    "date": r.created})
                data = {"name": quiz.name,
                        "id": quiz.quiz_ID,
                        "QA": QA,
                        "results": results}
            except:
                return Response("ID Error!", status=400)
            return JsonResponse(data)
        else:
            return Response("Not authorized!", status=401)
        
    
class QuizPageAPI(GenericAPIView):
    serializer_class = QuizPageserializer
    schema = QuizPageSchema()

    def get(self,request,quiz_id):
        try:
            quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
            questions = get_list_or_404(Question, quiz=quiz)
            QA = []
            for q in questions:
                answers = []
                for a in get_list_or_404(Answer, question=q):
                    answers.append(a.text)
                QA.append({"question": q.text,
                            "answers": answers})
            data = {"name": quiz.name,
                    "id": quiz.quiz_ID,
                    "QA": QA}
        except:
            return Response("ID Error!", status=400)
        return JsonResponse(data)
    
    def post(self,request,quiz_id):
        body = json.loads(request.body)
        try:
            quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        except:
            return Response("ID Error!", status=400)
        try:
            questions = get_list_or_404(Question, quiz=quiz)
            questions_len = len(questions)
            correct_question = 0
            i = 0
            for q in questions:
                answers = Answer.objects.filter(question=q)
                if answers.get(text=body["answers"][i]).is_correct:
                    correct_question += 1
                i += 1

            score = round((correct_question / questions_len) *100, 2)
            Result.objects.create(taker_name=body['taker_name'], quiz=quiz, score=score)

        except:
            return Response("Request body Error!", status=400)
        return JsonResponse({"score": score})