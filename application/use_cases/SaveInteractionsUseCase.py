import uuid

from domain.Question import Question
from domain.repository.QuestionRepository import QuestionRepository


class SaveInteractionUseCase:

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository
        pass

    def execute(self, question_user: str, answer: str, type: str):
        question_id = str(uuid.uuid4())
        question_entity = Question(question_id, question_user, answer, type)
        self.question_repository.save(question_entity)
