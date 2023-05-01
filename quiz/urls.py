from django.urls import path
from .views import CreateQuiz, QuizDetails, QuizPage

urlpatterns = [
    path('create', CreateQuiz.as_view(), name='create_quiz'),
    path('details/<str:quiz_id>/', QuizDetails.as_view()),
    path('start/<str:quiz_id>/', QuizPage.as_view()),
]