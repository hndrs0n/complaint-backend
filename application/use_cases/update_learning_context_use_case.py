from typing import Any, Dict
from application.ports.student_reposity import StudentRepository

class UpdateLearningContextUseCase:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def execute(self, student_id: str, updates: Dict[str, Any]) -> None:
        student = self.student_repository.get(student_id)
        if student is None:
            raise ValueError(f"Student with id {student_id} not found")
        student.update_learning_context(updates)
        self.student_repository.save(student)