from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from questions.models import User, Answers, Questions
from questions.serializers import QuestionsSerializer


@api_view(["POST"])
@permission_classes([AllowAny,])
def register(request):
    """
    Register new user 
    """
    try:
        User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password'), 
            email=request.data.get('email')
        )
        return Response({'Succefully registered, proceed to login'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'Invalid Credentials, try again'}, status=status.HTTP_409_CONFLICT)

@api_view(['POST'])
@permission_classes([AllowAny,])
def login(request):
    """
    Authenticate user credential to be able to login 
    """
    user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
    if user is not None:
        # Generate and return the JWT 
        token = RefreshToken.for_user(user)
        data = {
            "access-token": str(token.access_token),
            "refresh-token": str(token)
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_list(request):
    """
    Create new question and list all questions
    """
    user = request.user

    if request.method == 'GET':
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = QuestionsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def question_detail(request, question_id):
    """
    Retrieve and delete a question
    """
    try: 
        question = Questions.objects.prefetch_related('answers_set').get(pk=question_id)
    except Questions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionsSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)
     
    elif request.method == 'DELETE':
        if request.user.id == question.id: 
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET', 'POST'])  
@authentication_classes([])
def answer_question(request, question_id):
    """
    """
    pass 

@api_view(['GET', 'POST'])  
@authentication_classes([])
def answer_detail(reqeust, question_id, answer_id):
    pass
  
