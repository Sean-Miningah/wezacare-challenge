from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .models import Answers, Questions, User
from .serializers import AnswersSerializer, QuestionsSerializer, UserSerializer


class QuestionsTest(APITestCase):
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
        response = self.client.get(self.url)
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
        self.assertEqual(response.data['description'], test_description)
        self.assertEqual(response.data['author'], self.user.username)

        # Test updating a question 
        response = self.client.put(url, {'description': 'Updated question'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test deleting a question 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Questions.objects.filter(pk=question.id).exists())

    def test_answer_questions(self):
        """
        Test saving of answers to existing questions
        """
        test_description = "Test Description"
        question = Questions.objects.create(author=self.user, description=test_description)
        url = reverse('question-answers', args=[question.id,])

        # Test post a valid answer 
        data = {
            "description": "Test Answer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test posting an invalid answer 
        data = {}
        response = self.client(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test posting wrong invalid question answering 
        url = reverse('question-answers', args=[3000000])
        response = self.client(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # def tearDown(self):
    #     self.user.delete
    

    # def test_get_question_list(self):
        
    #     url = reverse('app-questions')

    #     # test empty response
    #     response = self.client.get(url)
    #     data = response.content.decode('utf-8')
    #     self.assertEqual(data, '[]')

    #     # test list of questions
    #     Questions.objects.create(
    #         author=self.user, 
    #         description="test_description"
    #     )
    #     Questions.objects.create(
    #         author=self.user, 
    #         description="test_description2"
    #     )

    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     test_client = APIClient()

    #     # test posting empty objects
        

    #     response =  self.client.post(url, {}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     #test getting questions
    #     data = {
    #         "description": "Test Description"
    #         }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code,  status.HTTP_201_CREATED,)

    # def test_question_detail(self):
    #     """
    #     Test question_detail url
    #     """
    #     question = Questions.objects.create(author=self.user, description=self.description)
    #     url = reverse("question-details", kwargs={'question_id': question.id} )

    #     # test right question_id    
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # test update question_id
    #     data = {
    #         "description": "Put Request Description"

    #     }
    #     response = self.client.put(url, data, format='json')
    #     data_id = response.json()["id"]
    #     self.assertEqual(int(data_id), question.id)
        
    #     # test retrieving a question
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #     # test wrong question_id
    #     failed_id = 100
    #     url = reverse("question-details", kwargs={"question_id": failed_id})
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    # def test_  
        

