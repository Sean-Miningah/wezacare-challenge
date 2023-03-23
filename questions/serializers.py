from rest_framework import serializers

from questions.models import User, Questions, Answers


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Questions 
        fields = '__all__'


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers 
        fields = '__all__'

