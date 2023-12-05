class Complaint:
    def __init__(self, id, complaint, answer, type):
        self.id = id
        self.complaint = complaint
        self.answer = answer
        self.type = type

    def get_question(self):
        return self.complaint

    def get_answer(self):
        return self.answer

    def get_id(self):
        return self.id

    def set_complaint(self, complaint):
        self.complaint = complaint

    def set_answer(self, answer):
        self.answer = answer

    def set_id(self, id):
        self.id = id

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

