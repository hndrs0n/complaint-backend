from abc import ABC, abstractmethod
from domain.Question import Question


class QuestionRepository(ABC):

    @abstractmethod
    def save(self, question: Question) -> None:
        pass

