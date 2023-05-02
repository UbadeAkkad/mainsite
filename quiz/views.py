from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Quiz, Question, Answer
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64

class CreateQuiz(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'quiz/create_quiz.html')

    def post(self, request):
        quiz = Quiz.objects.create(name=request.POST['quiz_name'], user=self.request.user)
        i = 0
        for Q in request.POST.getlist('question'):
            question = Question.objects.create(quiz=quiz, text=Q)
            i += 1
            AnswerList = request.POST.getlist(f'question_{i}_answer')
            for A in AnswerList:
                is_correct = request.POST.get(f'question_radio_{i}') == A
                Answer.objects.create(question=question, text = A, is_correct=is_correct)

        return redirect("quiz_details", quiz_id=str(quiz.quiz_ID))
    
class QuizDetails(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        start_url = "https://ubade.pythonanywhere.com/quiz/start/" + str(quiz.quiz_ID)
        img = qrcode.make(start_url)
        buff = BytesIO()
        img.save(buff)
        img_str = base64.b64encode(buff.getvalue())
        img_str = img_str.decode("utf-8")
        questions = get_list_or_404(Question, quiz=quiz)
        QA = []
        for q in questions:
            answers = []
            for a in get_list_or_404(Answer, question=q):
                answers.append({"answer": a.text,
                                 "correct": a.is_correct})
            QA.append({"question": q.text,
                        "answers": answers})
        
        return render(request,'quiz/quiz_details.html', {"quiz": quiz, "questions": QA, "url": start_url, "QR": img_str})
    
class QuizPage(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        return HttpResponse(quiz.name)
    
    def post(self,request):
        pass
