from abc import ABC, abstractmethod
from typing import Optional
from domain.Student import Student

class StudentRepository(ABC):

    @abstractmethod
    def get(self, student_id: str) -> Optional[Student]:
        pass

    @abstractmethod
    def save(self, student: Student) -> None:
        pass