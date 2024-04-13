import random

from django.core.management.base import BaseCommand
from QuizGame.models import Question


class Command(BaseCommand):
    def handle(self, *args, **options):
        questions = Question.objects.all()
        for question in questions:
            question_answers = question.answers.split(',')
            correct_answer = question_answers[question.correct_answer]
            random.shuffle(question_answers)
            new_correct_answer = question_answers.index(correct_answer)
            question.answers = ",".join(question_answers)
            question.correct_answer = new_correct_answer
            question.save()
