from domain.repository.ComplaintRepository import ComplaintRepository
from domain.entitites.Complaint import Complaint
from firebase_admin import db

import os


class FirebaseComplaintRepository(ComplaintRepository):

    def __init__(self):
        self.db = db.reference(os.getenv('FIREBASE_DB_REFERENCE_COMPLAINT'))

    def save(self, complaint: Complaint) -> None:
        complaint_data = {
            'id': complaint.id,
            'question': complaint.complaint,
            'answer': complaint.answer,
            'type': complaint.type
        }
        self.db.child(complaint.id).set(complaint_data)
