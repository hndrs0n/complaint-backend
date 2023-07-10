from ..prompt_strategy import PromptStrategy

class SumasLlevandoPrompt(PromptStrategy):
    def build_prompts(self, student, message, problem):
        prompts = {
            'explicacion': (
                f"Estás asistiendo a {student.name}, un estudiante de segundo grado de primaria que "
                f"ha formulado la siguiente pregunta: \"{message['question']}\". Por favor, proporciona una "
                f"explicación del concepto de 'sumas llevando' de manera clara y fácil de entender para un niño de segundo grado."
            ),
            'problema': (
                f"Ahora, por favor genera un problema específico relacionado con el concepto de 'sumas llevando' que el estudiante "
                f"{student.name} preguntó, \"{message['question']}\". Recuerda, el problema debe ser relevante "
                f"y apropiado para un estudiante de segundo grado. La explicación anterior fue: "
            ),
            'alternativas': (
                f"Genial. Ahora, por favor genera algunas alternativas de respuesta para el problema de 'sumas llevando' que has propuesto. "
                f"Incluye tanto la respuesta correcta como dos respuestas incorrectas. El problema propuesto fue: {problem}"
            ),
            'explicacion_problema': (
                f"Perfecto. Ahora, por favor genera una explicación dinámica para el problema de 'sumas llevando' que has propuesto. "
                f"Esta debe ser una explicación detallada del procedimiento para resolver el problema, con un enfoque en "
                f"hacerlo atractivo y comprensible para un estudiante de segundo grado. El problema propuesto fue: {problem}"
            ),
            'motivacion_respuesta_incorrecta': (
                f"Finalmente, por favor genera un mensaje amigable y motivador que el asistente puede dar al estudiante "
                f"{student.name} en caso de que él o ella elijan una respuesta incorrecta al problema de 'sumas llevando' propuesto. El problema propuesto fue: {problem}"
            ),
        }

        return prompts
