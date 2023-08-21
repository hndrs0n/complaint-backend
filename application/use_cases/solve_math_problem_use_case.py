from application.ports.student_reposity import StudentRepository
from infrastructure.api.chat_gpt_adpater import ChatGPTAdapter
from domain.Student import Student
from .add_interaction_use_case import AddInteractionUseCase

class SolveMathProblemUseCase:
    def __init__(self, student_repository: StudentRepository, chat_gpt_adapter: ChatGPTAdapter):
        self.student_repository = student_repository
        self.chat_gpt_adapter = chat_gpt_adapter
        self.add_interaction_use_case = AddInteractionUseCase(student_repository)

    def execute(self, student_id: str, question: StudentRepository):
        student = self.student_repository.get(student_id)
        if not student:
            raise Exception("Student not found")

        answer = self.chat_gpt_adapter.generate_response(student, question)
        self.add_interaction_use_case.execute(student, question, answer)

        return answer
