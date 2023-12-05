import uuid

from domain.entitites.Complaint import Complaint
from domain.repository.ComplaintRepository import ComplaintRepository


class SaveInteractionUseCase:

    def __init__(self, complaint_repository: ComplaintRepository):
        self.complaint_repository = complaint_repository
        pass

    def execute(self, complaint: str, answer: str, type: str):
        complaint_id = str(uuid.uuid4())
        complaint_entity = Complaint(complaint_id, complaint, answer, type)
        self.complaint_repository.save(complaint_entity)
