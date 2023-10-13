class Student:
    def __init__(self, id, name,interaction_history=None):
        self.id = id
        self.name = name
        self.interaction_history = interaction_history or []

    def update_learning_context(self, updates):
        self.learning_context.update(updates)

    def get_learning_context(self):
        return self.learning_context

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average_grade(self):
        return sum(self.grades) / len(self.grades) if self.grades else None

    def add_interaction(self, question, answer):
        self.interaction_history.append((question, answer))