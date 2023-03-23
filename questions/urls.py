from django.urls import path 

from questions import views


urlpatterns = [
    path('questions/', views.question_list),
    path('questions/<int:question_id>', views.question_detail),
    path('questions/<int:question_id>/answers', views.answer_question),
    path('questions/<int:question_id>/answers/<int:answer_id', views.answer_detail)
]