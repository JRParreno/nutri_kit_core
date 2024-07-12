from rest_framework import serializers
from .models import Question, Category, Answer


class TriviaCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializers(serializers.ModelSerializer):
    category = TriviaCategorySerializers()
    answers = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = '__all__'
    
    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        return AnswerSerializer(answers, many=True).data