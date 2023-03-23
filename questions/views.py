from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from questions.models import Questions, Answers
from questions.serializers import QuestionsSerializer


def register(reqeust):
    pass


def login(request):
    pass


@api_view(['GET', 'POST'])
def question_list(request):
    """
    List all questions
    """

    if request.method == 'GET':
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, question_id):
    """
    Retrieve, update or delete a question
    """
    try: 
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionsSerializer(question)
        return Response(serializer.data)
                        
    elif request.method == 'PUT':
        serializer = QuestionsSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def answer_question(request, question_id):
    pass 


def answer_detail(reqeust, question_id, answer_id):
    pass
  
