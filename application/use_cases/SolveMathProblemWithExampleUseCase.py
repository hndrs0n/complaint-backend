from application.ports.student_reposity import StudentRepository
from domain.repository.QuestionRepository import QuestionRepository
from infrastructure.api.chat_gpt_adpater import ChatGPTAdapter
from .SaveInteractionsUseCase import SaveInteractionUseCase

class SolveMathProblemWithExampleUseCase:
    def __init__(self, question_repository: QuestionRepository, chat_gpt_adapter: ChatGPTAdapter):
        self.add_interaction_use_case = SaveInteractionUseCase(question_repository)
        self.question_repository = question_repository
        self.chat_gpt_adapter = chat_gpt_adapter

    def execute(self, message):

        answer = self.chat_gpt_adapter.generate_response(message)
        self.add_interaction_use_case.execute(message, answer, "math")

        return answer
