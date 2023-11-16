import random
import re
import json

class PatronesNumericos:
    def __init__(self, adapter):
        self.adapter = adapter
        self.sequence = []

    def set_number_sequence_from_message(self, message):
        self.sequence = [int(num) for num in re.findall(r'\b\d+\b', message)] if message else []

    def find_step_in_sequence(self):
        if len(self.sequence) > 1:
            steps = [self.sequence[i+1] - self.sequence[i] for i in range(len(self.sequence) - 1)]
            if len(set(steps)) == 1:
                return steps[0]
        return None

    def generar_respuesta(self, message):
        self.set_number_sequence_from_message(message)
        step = self.find_step_in_sequence()

        if not self.sequence or step is None:
            step = random.randint(1, 10)
            self.sequence = self.generate_number_sequence(step)

        explanation_prompt = (
            f"Un estudiante preguntó \"{message}\", explica el concepto de patrones numéricos. "
            f"Usa la secuencia {self.sequence} para la explicación, donde el paso del patrón es {step}. "
            f"La explicación debe ser adecuada para niños de 7 años, simple y divertida. "
            f"La respuesta debe estar en formato JSON, sin saltos de línea:"
            f"{{"
            f"  \"saludo\": \"¡Hola, pequeño matemático!\","
            f"  \"tema\": \"Hoy vamos a explorar el maravilloso mundo de los patrones numéricos.\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Observa esta secuencia: {self.sequence}. ¿Puedes descubrir el patrón?\","
            f"    \"pasos\": [\"Primero, mira la diferencia entre los números consecutivos.\", \"Identifica si hay que sumar o restar.\", \"Usa el patrón para predecir el siguiente número en la secuencia.\"],"
            f"    \"resultado\": \"El patrón es sumar {step} cada vez.\""
            f"  }},"
            f"  \"conclusion\": \"¿Ves? Con práctica, puedes encontrar patrones en cualquier lugar.\","
            f"  \"sugerencia_practica\": \"Prueba con otras secuencias o incluso crea las tuyas para seguir practicando.\""
            f"}}"
        )

        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)

        try:
            explanation = json.loads(explanation_json)
        except json.JSONDecodeError:
            explanation = {"error": "La respuesta recibida no está en formato JSON"}

        return {
            "response": {
                "type": "patronesNumericos",
                "content": explanation,
                "data": {
                    "sequence": self.sequence,
                    "step": step
                }
            }
        }

    def generate_number_sequence(self, step):
        start = random.randint(1, 10)
        return [start + i * step for i in range(5)]

