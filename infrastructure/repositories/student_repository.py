from application.ports.student_reposity import StudentRepository
from domain.Student import Student
from firebase_admin import db
from typing import Optional
import os



class FirebaseStudentRepository(StudentRepository):

    def __init__(self):
        self.db = db.reference(os.getenv('FIREBASE_DB_REFERENCE'))

    def get(self, student_id: str) -> Optional[Student]:
        result = self.db.child(student_id).get()
        if result:
            return Student(
                id=result['id'], 
                name=result['name'], 
                level=result['level'], 
                learning_context=result.get('learning_context'), 
                grades=result.get('grades'), 
                learning_preferences=result.get('learning_preferences'), 
                interaction_history=result.get('interaction_history')
            )
        else:
            return None

    def save(self, student: Student) -> None:
        student_data = {
            'id': student.id,
            'name': student.name,
            'level': student.level,
            'learning_context': student.get_learning_context(),
            'grades': student.grades,
            'learning_preferences': student.learning_preferences,
            'interaction_history': student.interaction_history,
        }
        self.db.child(student.id).set(student_data)
