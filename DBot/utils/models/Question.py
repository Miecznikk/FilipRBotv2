from dataclasses import dataclass

@dataclass
class Question:
    question: str
    answers: str
    correct_answer: int
    category: str
