import random
import re

class SumaLlevando:
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
        unit1 = random.randint(5, 9)
        unit2 = random.randint(10 - unit1, 9)
        
        # Elegir los dígitos de las decenas de manera aleatoria
        ten1 = random.randint(1, 9)
        ten2 = random.randint(1, 9)
        
        num1 = ten1 * 10 + unit1
        num2 = ten2 * 10 + unit2
        
        return num1, num2

    def get_carry_digits(self):

        numbers = [self.num1, self.num2]
        num1, num2 = [int(d) for d in str(numbers[0])[::-1]], [int(d) for d in str(numbers[1])[::-1]]
        carry = 0
        carry_digits = []

        for i in range(max(len(num1), len(num2))):
            n1 = num1[i] if i < len(num1) else 0
            n2 = num2[i] if i < len(num2) else 0

            if n1 + n2 + carry >= 10:
                carry = 1
                carry_digits.append(carry)
            else:
                carry = 0
                carry_digits.append(carry)

        return carry_digits[::-1]


    def generar_respuesta(self, message):
        self.set_numbers_from_message(message)

        numbers = [self.num1, self.num2]
        explanation_prompt = (
            f"Por favor un estudiante de segundo grado de primaria pregunto '{message}' , explica a  sobre la 'suma llevando'. "
            f"En ese caso usa estos numeros {numbers} para explicar este concepto. La explicación debe ser  para niños de 7 años, simple y divertida. Limita la respuesta a 150 palabras"
            f"La respuesta debe estar en el siguiente formato JSON, no agregues saltos de linea:"
            f"{{"
            f"  \"saludo\": \"Texto de saludo al estudiante o introducción breve',"
            f"  \"tema\": \"Descripción general del tema de suma llevando',"
            f"  \"ejemplo\": {{"
            f"    \"problema\": \"Problema o situación de suma llevando\","
            f"    \"pasos\": [\"Primer paso o acción\", \"Segundo paso o acción\", \"...\"],"
            f"    \"resultado\": \"Resultado final de la suma llevando\""
            f"  }},"
            f"  \"conclusion\": \"Conclusión general sobre suma llevando\","
            f"  \"sugerencia_practica\": \"Sugerencias para practicar suma llevando\""
            f"}}"
        )

        explanation_json = self.adapter.get_response_part(explanation_prompt, max_tokens=800)

        result = sum(numbers)

        carry_digits = self.get_carry_digits()
        return {
            "response": {
                "type": "sumaLlevando",
                "content": explanation_json,
                "data": {
                    "numbers": numbers,
                    "result": result,
                    "carry_digits": carry_digits
                }
            }
        }