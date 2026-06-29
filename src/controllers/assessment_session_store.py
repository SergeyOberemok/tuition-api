from dataclasses import dataclass

from src.core.assessment.assessment import IAssessment
from src.core.question_evaluation.question_evaluation import IQuestionEvaluation


@dataclass
class AssessmentSession:
    assessment: IAssessment | None = None
    assessment_item: IQuestionEvaluation | None = None


class AssessmentSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, AssessmentSession] = {}

    def get(self, sid: str) -> AssessmentSession:
        return self._sessions.setdefault(sid, AssessmentSession())

    def update(self, sid: str, **changes) -> AssessmentSession:
        session = self.get(sid)
        for key, value in changes.items():
            setattr(session, key, value)
        return session

    def reset(self, sid: str) -> None:
        self._sessions.pop(sid, None)
