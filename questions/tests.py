from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import Answers, Questions, User
from .serializers import AnswersSerializer, QuestionsSerializer, UserSerializer


class GetAllQuestions(APITestCase):
    """ Test module to GET all question API """

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