from application.use_cases import SaveInteractionUseCase
from domain.repository import QuestionRepository
from infrastructure.api import ChatGPTAdapterGeneric


class SolveMathProblemUseCase:
    def __init__(self, question_repository: QuestionRepository, chat_gpt_adapter_generic: ChatGPTAdapterGeneric):
        self.add_interaction_use_case = SaveInteractionUseCase(question_repository)
        self.question_repository = question_repository
        self.chat_gpt_adapter_generic = chat_gpt_adapter_generic

    def execute(self, message):

        answer = self.chat_gpt_adapter_generic.generate_response(message)
        self.add_interaction_use_case.execute(message, answer, "math")

        return answer
