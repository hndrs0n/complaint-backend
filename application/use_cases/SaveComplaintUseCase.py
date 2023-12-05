
from infrastructure.api.chat_gpt_adapater import ChatGPTAdapter
from .SaveInteractionsUseCase import SaveInteractionUseCase
from domain.repository.ComplaintRepository import ComplaintRepository

class SaveComplaintUseCase:
    def __init__(self, complaint_repository: ComplaintRepository, chat_gpt_adapter: ChatGPTAdapter):
        self.add_interaction_use_case = SaveInteractionUseCase(complaint_repository)
        self.complaint_repository = complaint_repository
        self.chat_gpt_adapter = chat_gpt_adapter

    def execute(self, message):

        topic = self.chat_gpt_adapter.generate_response(message, "")
        print(topic)
        answer = self.chat_gpt_adapter.generate_response(message, topic)
        print(answer)
        self.add_interaction_use_case.execute(message, answer, topic)


