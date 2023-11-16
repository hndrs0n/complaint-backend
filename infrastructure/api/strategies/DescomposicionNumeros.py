import random
import re
import json

class DescomposicionNumeros:
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
        num = random.randint(10, 999)
        return num

    def get_number_decomposition(self):
        hundreds = self.num // 100
        tens = (self.num - hundreds * 100) // 10
        ones = self.num % 10
        return hundreds, tens, ones

    def generar_respuesta(self, message):
        self.set_number_from_message(message)
        hundreds, tens, ones = self.get_number_decomposition()

        explanation_prompt = (
            f"Por favor, explica al estudiante el concepto de descomposición de números. "
            f"Usa el número {self.num} para la explicación. "
            f"La explicación debe ser adecuada para niños de 7 años, simple y divertida. "
            f"La respuesta debe estar en formato JSON, sin saltos de línea:"
            f"{{"
            f"  \"saludo\": \"¡Hola amigo matemático!\","
            f"  \"tema\": \"Explica de forma clara sobre el tema\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Plantea un problema con este numero  {self.num}\","
            f"    \"pasos\": [Explica los pasos, como si hubiera una grafico de bloques para reforzar el aprendizas],"
            f"    \"resultado\": \"Tienes {hundreds} centenas, {tens} decenas y {ones} unidades.\""
            f"  }},"
            f"  \"conclusion\": \"Ahora sabes cómo descomponer un número en sus partes.\","
            f"  \"sugerencia_practica\": \"¡Intenta con otros números para ser un experto descomponiendo!\""
            f"}}"
        )

        # Suponiendo que `self.adapter.get_response_part` es una llamada a un servicio que procesa el prompt y devuelve un JSON.
        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)
        explanation = json.loads(explanation_json)
        return {
            "response": {
                "type": "descomposicionNumeros",
                "content": explanation,
                "data": {
                    "num": self.num,
                    "hundreds": hundreds,
                    "tens": tens,
                    "ones": ones
                }
            }
        }