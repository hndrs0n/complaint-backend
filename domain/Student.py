class Student:
    def __init__(self, id, name, level, learning_context=None, grades=None, learning_preferences=None, interaction_history=None):
        self.id = id
        self.name = name
        self.level = level
        self.learning_context = learning_context or {}
        self.grades = grades or []
        self.learning_preferences = learning_preferences or {}
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

    def set_learning_preferences(self, preferences):
        self.learning_preferences = preferences