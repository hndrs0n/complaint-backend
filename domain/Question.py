class Question:
    def __init__(self, id, question, answer, type):
        self.id = id
        self.question = question
        self.answer = answer
        self.type = type

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_id(self):
        return self.id

    def set_question(self, question):
        self.question = question

    def set_answer(self, answer):
        self.answer = answer

    def set_id(self, id):
        self.id = id

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

