from django.core.management.base import BaseCommand
from QuizGame.models import Question


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_category = "Informatyka i internet"
        with open("QuizGame/management/commands/questions.txt", 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        for i in range(0, len(lines), 3):
            question_text = lines[i]
            answers = lines[i + 1]
            print(answers)
            if len(answers.split(',')) != 3:
                raise ValueError(f"Something went wrong deserializing answers: {lines[i + 1]}")
            correct_answer = lines[i + 2]
            try:
                correct_answer = int(correct_answer)
                if correct_answer > 2 or correct_answer < 0:
                    raise IndexError("Correct answer is beyond range")
            except ValueError:
                raise ValueError(f"Correct answer is not an integer")

            Question.objects.create(question=question_text, category=current_category,
                                    answers=answers, correct_answer=correct_answer)
