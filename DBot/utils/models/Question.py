from dataclasses import dataclass

@dataclass
class Question:
    question: str
    answers: list[str]
    correct_answer: int
    category: str
