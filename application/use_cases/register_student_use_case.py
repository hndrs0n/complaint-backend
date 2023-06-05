from domain.Student import Student
from application.ports.student_reposity import StudentRepository

class RegisterStudentUseCase:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def execute(self, id: str, name: str, level: str, learning_context=None, grades=None, learning_preferences=None, interaction_history=None):
        student = Student(id, name, level, learning_context, grades, learning_preferences, interaction_history)
        self.student_repository.save(student)