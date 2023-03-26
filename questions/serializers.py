from rest_framework import serializers

from questions.models import User, Questions, Answers


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Questions
        exclude = ('id',)


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers 
        fields = '__all__'

class QAnswerSerializer(serializers.ModelSerializer):
    """
    Answer serializer for QuestionAnswer serializer
    """

    class Meta: 
        model = Answers 
        fields = ['description']


class QuestionAnswersSerializer(serializers.Serializer):
    """
    Question Answers and it answers serializer 
    """
    question = QuestionsSerializer()
    answers = QAnswerSerializer(many=True, read_only=True)

