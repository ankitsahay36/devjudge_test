from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz_create),
    path('quiz/<quiz_id>', views.quiz_get),
    path('questions/<question_id>', views.question_get),
    path('questions/', views.question_create),
    path('quiz-questions/<quiz_id>', views.quiz_questions_get),
]