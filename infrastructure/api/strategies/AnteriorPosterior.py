import random
import re
import json

class AnteriorPosterior:
    def __init__(self, adapter):
        self.adapter = adapter
        self.num = None

    def set_number_from_message(self, message):
        # Intenta extraer un número del mensaje.
        match = re.search(r'\b(\d+)\b', message)
        if match:
            self.num = int(match.group(1))
        else:
            self.num = self.generate_example_number()

    def generate_example_number(self):
        # Generar un número aleatorio para el ejemplo.
        num = random.randint(2, 100)  # Evitamos el 1 para tener un anterior
        return num

    def get_previous_next(self):
        # Obtiene el número anterior y posterior al número dado.
        return self.num - 1, self.num + 1

    def generar_respuesta(self, message):
        self.set_number_from_message(message)
        previous_num, next_num = self.get_previous_next()

        explanation_prompt = (
            f"Por favor, explica al estudiante el concepto de número anterior y posterior. "
            f"Usa este número {self.num} para la explicación. "
            f"La explicación debe ser adecuada para niños de 7 años, simple y divertida. "
            f"La respuesta debe estar en formato JSON, sin saltos de línea:"
            f"{{"
            f"  \"saludo\": \"Realiza un saludo motivador al estudiante\","
            f"  \"audio\": \"Un texto que sera reproducido en audio explicando el problema y la solucion\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Crea un problema de número anterior y posterior con {self.num}\","
            f"    \"pasos\": [\"Describe una lista de pasos de manera resumida y clara para el nino\"],"
            f"    \"resultado\": \"El número anterior es {previous_num} y el posterior es {next_num}.\""
            f"  }}"
            f"}}"
        )

        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)
        explanation = json.loads(explanation_json)
        return {
            "response": {
                "type": "anteriorPosterior",
                "content": explanation,
                "data": {
                    "num": self.num,
                    "previous_num": previous_num,
                    "next_num": next_num
                }
            }
        }
