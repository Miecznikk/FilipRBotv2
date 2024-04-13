from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question
from .serializers import QuestionSerializer


class GetRandomQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, number_of_questions=None):
        if number_of_questions is None:
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        else:
            questions = Question.objects.order_by('?')[:number_of_questions]
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)

# Create your views here.
