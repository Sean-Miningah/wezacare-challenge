from django.urls import path 

from questions import views


urlpatterns = [
    path('questions/', views.question_list, name='app-questions'),
    path('questions/<int:question_id>', views.question_detail, name="question-details"),
    path('questions/<int:question_id>/answers', views.answer_question, name="qeustion-answer"),
    path('questions/<int:question_id>/answers/<int:answer_id', views.answer_detail, name="question-answer-update")
]