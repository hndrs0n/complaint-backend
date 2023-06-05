from application.ports.student_reposity import StudentRepository
from domain.Student import Student

class AddInteractionUseCase:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def execute(self, student: Student, question: str, answer: str):
        student.add_interaction(question, answer)
        self.student_repository.save(student)