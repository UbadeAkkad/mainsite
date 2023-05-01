from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Quiz, Question, Answer
from django.http import HttpResponse

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
                answer = Answer.objects.create(question=question, text = A, is_correct=is_correct)
        
        return HttpResponse(str(request.POST))
    
class QuizDetails(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        questions = get_list_or_404(Question, quiz=quiz)
        QA = []
        for q in questions:
            answers = []
            for a in get_list_or_404(Answer, question=q):
                answers.append({"answer": a.text,
                                 "correct": a.is_correct})
            QA.append({"question": q.text,
                        "answers": answers})
        
        return render(request,'quiz/quiz_details.html', {"quiz": quiz, "questions": QA})
    
class QuizPage(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        return HttpResponse(quiz.name)
    
    def post(self,request):
        pass
