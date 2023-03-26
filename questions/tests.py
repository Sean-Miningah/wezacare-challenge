from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .models import Answers, Questions, User
from .serializers import AnswersSerializer, QuestionsSerializer, UserSerializer


class AuthorisationTest(APITestCase):
    """
    Test module to test user registration and user login 
    """

    def setUp(self):
        self.username = 'test-user'
        self.password = 'testPassword'
        self.data = {
            'username': self.username,
            'password': self.password
        }


    def test_registration(self):
        url = reverse('registration')

        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_login(self):
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
    """ 
    Test module for creating questions and get questions 
    """

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

        self.url = reverse('app-questions')

    
    def test_list_questions(self):
        """
        Test listing all questions
        """

        # test empty response 
        url = reverse('app-questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # test list of questions 
        question1 = Questions.objects.create(author=self.user, description="test_description")
        question2 = Questions.objects.create(author=self.user, description="test_description")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, question1.description)
        self.assertContains(response, question2.author.username)

    def test_create_question(self):
        """
        Test creating a new question
        """
        url = reverse('app-questions')

        data = {"description": "Test Description"}

        # test valid data 
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Questions.objects.count(), 1)
        question = Questions.objects.first()
        self.assertEqual(question.description, data['description'])
        self.assertEqual(question.author, self.user)

        # test invalid data 
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_question_detail(self):
        """
        Test retrieving, updating and deleting a question 
        """
        test_description = "Test Description"
        question = Questions.objects.create(author=self.user, description=test_description) 
        url = reverse('question-details', args=[question.id])

        # Test retrieving a question 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('question', response.data)
        self.assertIsInstance(response.data['answers'], list)

        # Test updating a question 
        response = self.client.put(url, {'description': 'Updated question'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test deleting a question 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Questions.objects.filter(pk=question.id).exists())




class TestAnswers(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.email = 'test@email.com'
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.user2 = User.objects.create_user(
            username="user2test",
            password="user2passwordtest",
            email="user2@test.com"
        )
        self.access_token = str(
            AccessToken.for_user(self.user)
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token
        )

        self.url = reverse('app-questions')
    
    def tearDown(self):
        self.user.delete

    def test_answer_questions(self):
        """
        Test saving of answers to existing questions
        """
        test_description = "Test Description"
        question = Questions.objects.create(author=self.user, description=test_description)
        url = reverse('question-answer', args=[question.id,])

        # Test post a valid answer wrong question 
        valid_data = {
            "description": "Test Answer"
        }
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test post a valid answer to right question
        valid_question = Questions.objects.create(author=self.user2, description=test_description)
        url = reverse('question-answer', args=[valid_question.id,])
        valid_response = self.client.post(url, valid_data, format='json')
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)

        # Test posting an invalid answer 
        invalid_data = {}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test posting wrong invalid question answering 
        invalid_url = reverse('question-answer', args=[3000000])
        response = self.client.post(invalid_url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
class TestAnswerDetail(APITestCase):
    
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
        self.question = Questions.objects.create(
            description="Test Description",
            author=self.user
        )

        self.answer = Answers.objects.create(
            description="Test Answer",
            author=self.user,
            question=self.question

        )

        self.url = reverse(
            'question-answer-detail', 
            # kwargs={
            #     "question_id":self.question.id, 
            #     "answer_id": self.answer.id
            # }
            args = [self.question.id, self.answer.id]
        )
    
    def tearDown(self):
        self.user.delete
        self.question.delete


    def test_answer_detail(self):
        """
        Test the updating and deleting of answers to questions 
        """

        # testing update with valid parameters
        valid_data = {
            "description": "Updated Test Description"
        }

        response = self.client.put(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testing updating with invalid parameters 
        invalid_data = {
            "descvimption": "Updated Invalid Test Description"
        }

        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # testing deleting answer 
        delete_response = self.client.delete(self.url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # testing deleting invalid answer 

        invalid_delete = self.client.delete(self.url)
        self.assertEqual(invalid_delete.status_code, status.HTTP_404_NOT_FOUND)
        url = reverse('question-answer-detail', kwargs={"question_id": 12020, "answer_id": 2343})
        invalid_delete = self.client.delete(url)
        self.assertEqual(invalid_delete.status_code, status.HTTP_404_NOT_FOUND)

