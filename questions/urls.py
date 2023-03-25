from django.urls import path 

from questions import views


urlpatterns = [
    path('', views.question_list, name='app-questions'),
    path('<int:question_id>', views.question_detail, name="question-details"),
    path('questions/<int:question_id>/answers', views.answer_question, name="question-answer"),
    path('questions/<int:question_id>/answers/<int:answer_id', views.answer_detail, name="question-answer-update")
]