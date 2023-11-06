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
            f"  \"saludo\": \"¡Hola, pequeño matemático!\","
            f"  \"tema\": \"Hoy vamos a descubrir qué número se esconde antes y después de otro.\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Si tenemos el número {self.num}, ¿cuál es el número anterior y el posterior?\","
            f"    \"pasos\": [\"Para el anterior, solo necesitamos restar uno.\", \"Para el posterior, añadimos uno.\", \"¡Es como un juego de saltos hacia adelante y hacia atrás!\"],"
            f"    \"resultado\": \"El número anterior es {previous_num} y el posterior es {next_num}.\""
            f"  }},"
            f"  \"conclusion\": \"¡Muy bien! Ahora sabes qué número viene antes y después.\","
            f"  \"sugerencia_practica\": \"Intenta con otros números o con tus juguetes para practicar.\""
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
