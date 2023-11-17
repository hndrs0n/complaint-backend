import random
import re
import json

class RestasPrestando:
    def __init__(self, adapter):
        self.adapter = adapter
        self.num1 = None
        self.num2 = None

    def set_numbers_from_message(self, message):
        # Intenta extraer un par de números de la message.
        match = re.search(r'(\d+)[^\d]+(\d+)', message)
        if match:
            self.num1, self.num2 = int(match.group(1)), int(match.group(2))
        else:
            self.num1, self.num2 = self.generate_example_numbers()

    def generate_example_numbers(self):
        # Elegir los dígitos de las unidades de manera que su suma sea mayor que 9
        ten1 = random.randint(2,
                              9)  # Asegura que la cifra de las decenas de num1 sea al menos 2 para permitir el préstamo
        ten2 = random.randint(1, ten1 - 1)  # Asegura que la cifra de las decenas de num2 sea menor que la de num1

        # Elegir los dígitos de las unidades de manera que la cifra de num2 sea mayor que la cifra de num1
        unit1 = random.randint(0, 4)
        unit2 = random.randint(5, 9)

        num1 = ten1 * 10 + unit1
        num2 = ten2 * 10 + unit2

        return num1, num2


    def get_borrow_digits(self):
        numbers = [self.num1, self.num2]
        num1, num2 = [int(d) for d in str(numbers[0])[::-1]], [int(d) for d in str(numbers[1])[::-1]]
        borrow = 0
        borrow_digits = []

        for i in range(max(len(num1), len(num2))):
            n1 = num1[i] if i < len(num1) else 0
            n2 = num2[i] if i < len(num2) else 0

            if n1 - borrow < n2:
                borrow = 1
                borrow_digits.append(borrow)
            else:
                borrow = 0
                borrow_digits.append(borrow)

        return borrow_digits[::-1]


    def generar_respuesta(self, message):
        self.set_numbers_from_message(message)

        numbers = [self.num1, self.num2]
        explanation_prompt = (
            f"Por favor un estudiante de segundo grado de primaria pregunto '{message}' , explica a  sobre la 'restas prestando'. "
            f"En ese caso usa estos numeros {numbers} para explicar este concepto. La explicación debe ser  para niños de 7 años, simple y divertida. Limita la respuesta a 150 palabras"
            f"La respuesta debe estar en el siguiente formato JSON:"
            f"{{"
            f"  \"saludo\": \"Texto de saludo o introducción breve',"
            f"  \"audio\": \"Un texto que sera reproducido en audio explicando el problema y la solucion\","
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Problema o situación de suma llevando\","
            f"    \"pasos\": [\"Primer paso o acción\", \"Segundo paso o acción\", \"...\"],"
            f"    \"resultado\": \"Resultado final de la suma llevando\""
            f"  }}"
            f"}}"
        )

        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)
        explanation = json.loads(explanation_json)
        result = self.num1 - self.num2

        borrow_digits = self.get_borrow_digits()
        return {
            "response": {
                "type": "restaPrestando",
                "content": explanation,
                "data": {
                    "numbers": numbers,
                    "result": result,
                    "borrow_digits": borrow_digits  # Cambio carry_digits por borrow_digits
                }
            }
        }