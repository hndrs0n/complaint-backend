class PromptStrategy:
    def build_prompts(self, student, message, problem):
        prompts = {
            'explicacion': self.build_explanation_prompt(student, message),
            'problema': self.build_problem_prompt(student, message),
            'alternativas': self.build_alternatives_prompt(student, problem),
            'explicacion_problema': self.build_problem_explanation_prompt(student, problem),
            'motivacion_respuesta_incorrecta': self.build_motivation_prompt(student, problem)
        }
        return prompts

    def build_explanation_prompt(self, student, message):
        return (
            f"Estás asistiendo a {student.name}, un estudiante de segundo grado de primaria que "
            f"ha formulado la siguiente pregunta: \"{message['question']}\". Por favor, proporciona una "
            f"explicación del concepto de '{self.get_topic()}' de manera clara y fácil de entender para un niño de segundo grado."
        )

    def build_problem_prompt(self, student, message):
        return (
            f"Ahora, por favor genera un problema específico relacionado con el concepto de '{self.get_topic()}' que el estudiante "
            f"{student.name} preguntó, \"{message['question']}\". Recuerda, el problema debe ser relevante "
            f"y apropiado para un estudiante de segundo grado. La explicación anterior fue: "
        )

    def build_alternatives_prompt(self, student, problem):
        return (
            f"Genial. Ahora, por favor genera algunas alternativas de respuesta para el problema de '{self.get_topic()}' que has propuesto. "
            f"Incluye tanto la respuesta correcta como dos respuestas incorrectas. El problema propuesto fue: {problem}"
        )

    def build_problem_explanation_prompt(self, student, problem):
        return (
            f"Perfecto. Ahora, por favor genera una explicación dinámica para el problema de '{self.get_topic()}' que has propuesto. "
            f"Esta debe ser una explicación detallada del procedimiento para resolver el problema, con un enfoque en "
            f"hacerlo atractivo y comprensible para un estudiante de segundo grado. El problema propuesto fue: {problem}"
        )

    def build_motivation_prompt(self, student, problem):
        return (
            f"Finalmente, por favor genera un mensaje amigable y motivador que el asistente puede dar al estudiante "
            f"{student.name} en caso de que él o ella elijan una respuesta incorrecta al problema de '{self.get_topic()}' propuesto. El problema propuesto fue: {problem}"
        )

    def get_topic(self):
        raise NotImplementedError("Las subclases deben implementar este método")
