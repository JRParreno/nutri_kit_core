from rest_framework import generics, permissions, response, status
from .models import Category, Question, Answer
from .serializers import QuestionSerializers

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated,]