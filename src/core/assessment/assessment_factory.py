from abc import ABC

from src.core.assessment.assessment import IAssessment, Assessment
from src.core.question_evaluation.question_evaluation_factory import QuestionEvaluationFactory


class AssessmentFactory(ABC):
    @staticmethod
    def create(questions) -> IAssessment:
        evaluations = [QuestionEvaluationFactory.create(question, operation) for question, operation in questions]
        return Assessment(evaluations)

    @staticmethod
    def create_addition_assessment(questions) -> IAssessment:
        evaluations = [QuestionEvaluationFactory.create(question, '+') for question in questions]
        return Assessment(evaluations)
