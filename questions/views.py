from django.conf import settings
from django.contrib.auth import authenticate
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
        data = request.data
        data['author'] = user.id
        serializer = QuestionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
    

@api_view(['GET', 'POST'])  
@authentication_classes([])
def answer_question(request, question_id):
    pass 

@api_view(['GET', 'POST'])  
@authentication_classes([])
def answer_detail(reqeust, question_id, answer_id):
    pass
  
