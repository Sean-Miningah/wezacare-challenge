from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .models import Answers, Questions, User
from .serializers import AnswersSerializer, QuestionsSerializer, UserSerializer


class GetAllQuestions(APITestCase):
    """ Test module to test user registration and user loginI """

    def setUp(self):
        self.username = 'test-user'
        self.password = 'testPassword'
        self.data = {
            'username': self.username,
            'password': self.password
        }
        # self.test_user = User.objects.create(
        #     username="test-username", email="test@gmail.com", password="testpassword"
        # )
        # self.question_one = Questions.objects.create(
        #     author = self.test_user, 
        #     description = "Test_description_one"
        # )
        # self.question_two = Questions.objects.create(
        #     author = self.test_user,
        #     description = "Test_description_two"
        # )

    def test_user_registration(self):
        url = reverse('registration')

        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_login(self):
        username = "testor"
        password = "passi"
        User.objects.create_user(username=username, password=password)
        url = reverse('login')


        response = self.client.post(url, {"username":username, "password":password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        invalid_credentials = {
            "username": "BadUser",
            "password": "testPassword",
            "email": "bad@email.com"
        }
        response = self.client.post(url, invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionsTest(APITestCase):
    """ Test module for creating questions and get questions """

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.email = 'test@email.com'
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.access_token = str(
            AccessToken.for_user(self.user)
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token
        )

    def tearDown(self):
        self.user.delete
    

    def test_get_questions(self):
        Questions.objects.create(
            author=self.user, 
            description="test_description"
        )
        Questions.objects.create(
            author=self.user, 
            description="test_description2"
        )

        url = reverse('questions')
        response = self.client.get(url)
        other_client = APIClient()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        
        

