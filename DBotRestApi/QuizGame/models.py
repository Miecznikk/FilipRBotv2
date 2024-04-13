from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=100)
    answers = models.CharField(max_length=255)
    correct_answer = models.SmallIntegerField()
    category = models.CharField(max_length=50)

# Create your models here.
