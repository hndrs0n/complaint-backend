from domain.repository.QuestionRepository import QuestionRepository
from domain.Question import Question
from firebase_admin import db

import os


class FirebaseQuestionRepository(QuestionRepository):

    def __init__(self):
        self.db = db.reference(os.getenv('FIREBASE_DB_REFERENCE'))

    def save(self, question: Question) -> None:
        question_data = {
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'type': question.type
        }
        self.db.child(question.id).set(question_data)
