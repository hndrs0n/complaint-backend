import random
import re
import json

class ComparacionNumeros:
    def __init__(self, adapter):
        self.adapter = adapter
        self.num1 = None
        self.num2 = None

    def set_numbers_from_message(self, message):
        # Intenta extraer un par de números del mensaje.
        match = re.search(r'(\d+)[^\d]+(\d+)', message)
        if match:
            self.num1, self.num2 = int(match.group(1)), int(match.group(2))
        else:
            self.num1, self.num2 = self.generate_example_numbers()

    def generate_example_numbers(self):
        # Generar dos números aleatorios diferentes.
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        return num1, num2

    def get_comparison_result(self):
        # Determinar si los números son iguales, o identificar el mayor o el menor.
        if self.num1 == self.num2:
            return "son iguales"
        elif self.num1 > self.num2:
            return f"{self.num1} es mayor que {self.num2}"
        else:
            return f"{self.num1} es menor que {self.num2}"

    def generar_respuesta(self, message):
        self.set_numbers_from_message(message)
        comparison_result = self.get_comparison_result()

        explanation_prompt = (
            f"Por favor, explica al estudiante cómo comparar números. "
            f"Usa estos números {self.num1} y {self.num2} para explicar el concepto. "
            f"La explicación debe ser adecuada para niños de 7 años, simple y divertida. "
            f"Asegurate de devolver una estructura JSON, por nada agregues saltos de linea, devuelve tal cual el json:"
            f"{{"
            f"  \"saludo\": \"Texto de saludo al estudiante o introducción breve.\","
            f"  \"tema\": \"Descripción general del tema Comparar números\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Problema o situación de comparacion de numeros\","
            f"    \"pasos\": [Explica detallamente los pasos a seguir utilizando una recta numerica],"
            f"    \"resultado\": \"Resultado final de la comparacion\""
            f"  }},"
            f"  \"conclusion\": \"Conclusión general sobre comparar números\","
            f"  \"sugerencia_practica\": \"Sugerencias para practicar comparacion de numeros\""
            f"}}"
        )

        # Suponiendo que `self.adapter.get_response_part` es una llamada a un servicio que procesa el prompt y devuelve un JSON.
        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)
        explanation = json.loads(explanation_json)
        return {
            "response": {
                "type": "comparacionNumeros",
                "content": explanation,
                "data": {
                    "num1": self.num1,
                    "num2": self.num2,
                    "comparison_result": comparison_result
                }
            }
        }
