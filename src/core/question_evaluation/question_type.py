from enum import Enum


class QuestionType(str, Enum):
    CALCULATION = 'calculation'
    SEQUENCE = 'sequence'
    QUIZ = 'quiz'
