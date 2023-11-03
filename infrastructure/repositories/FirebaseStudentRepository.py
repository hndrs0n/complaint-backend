
from domain.Student import Student
from firebase_admin import db
from typing import Optional
import os

from domain.repository.StudentRepository import StudentRepository


class FirebaseStudentRepository(StudentRepository):

    def __init__(self):
        self.db = db.reference(os.getenv('FIREBASE_DB_REFERENCE'))

    def get(self, student_id: str) -> Optional[Student]:
        result = self.db.child(student_id).get()
        if result:
            return Student(
                id=result['id'], 
                name=result['name'],
                interaction_history=result.get('interaction_history')
            )
        else:
            return None

    def save(self, student: Student) -> None:
        student_data = {
            'id': student.id,
            'name': student.name,
            'interaction_history': student.interaction_history,
        }
        self.db.child(student.id).set(student_data)
