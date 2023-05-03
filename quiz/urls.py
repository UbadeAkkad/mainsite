from django.urls import path
from .views import CreateQuiz, QuizDetails, QuizPage
from django.views.generic.base import TemplateView

urlpatterns = [
    path('create', CreateQuiz.as_view(), name='create_quiz'),
    path('details/<str:quiz_id>/', QuizDetails.as_view(), name='quiz_details'),
    path('start/<str:quiz_id>/', QuizPage.as_view()),
    path('result/', TemplateView.as_view(template_name="quiz/quiz_result.html", content_type="text/html; charset=utf-8"), name='quiz_done'),
]