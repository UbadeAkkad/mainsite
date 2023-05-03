from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Quiz, Question, Answer, Result
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
        user_quizs = Quiz.objects.filter(user=request.user)
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
            
        start_url = "https://ubade.pythonanywhere.com/quiz/start/" + str(quiz.quiz_ID)
        #Create a QR code for the url
        img = qrcode.make(start_url)
        buff = BytesIO()
        img.save(buff)
        img_str = base64.b64encode(buff.getvalue())
        img_str = img_str.decode("utf-8")
        
        return render(request,'quiz/quiz_details.html', {"quiz": quiz, "questions": QA, "url": start_url, "QR": img_str})

class QuizPage(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        questions = get_list_or_404(Question, quiz=quiz)
        QA = []
        for q in questions:
            answers = []
            for a in get_list_or_404(Answer, question=q):
                answers.append(a.text)
            QA.append({"question": q.text,
                        "answers": answers})

        return render(request,'quiz/quiz_page.html', {"quiz": quiz, "questions": QA})

    def post(self,request, quiz_id):
        quiz = get_object_or_404(Quiz, quiz_ID=quiz_id)
        questions = get_list_or_404(Question, quiz=quiz)
        questions_len = len(questions)
        correct_question = 0
        i = 1
        for q in questions:
            answers = []
            for a in get_list_or_404(Answer, question=q):
                answers.append(a.is_correct)

            submitted_answer = request.POST.get(f'answer{i}')

            if submitted_answer == str(answers.index(True) + 1):
                correct_question += 1
            i += 1

        score = round((correct_question / questions_len) *100, 2)
        Result.objects.create(taker_name=request.POST['taker_name'], quiz=quiz, score=score)
        request.session["score"] = score
        return redirect("quiz_done")
