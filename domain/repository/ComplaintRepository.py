from abc import ABC, abstractmethod
from domain.entitites.Complaint import Complaint


class ComplaintRepository(ABC):

    @abstractmethod
    def save(self, question: Complaint) -> None:
        pass

