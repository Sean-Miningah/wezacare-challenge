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


class QuestionAnswersSerializer(serializers.ModelSerializer):
    """
    Question Answers and it answers serializer 
    """
    answers = QAnswerSerializer(many=True, read_only=True)

    class Meta: 
        model = Questions 
        fields = ['id', 'author', 'description', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('anwers')
        question = Questions.objects.create(**validated_data)
        for answer_data in answers_data: 
            Answers.objects.create(question=question, **answer_data)
        return question
