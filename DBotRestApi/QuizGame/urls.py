from django.urls import path
from .views import *

#api/quiz/

urlpatterns = [
    path('questions/', GetRandomQuestions.as_view(), name='all_questions'),
    path('questions/<int:number_of_questions>/', GetRandomQuestions.as_view(), name='random_questions'),
]
