import base64
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from gtts.lang import tts_langs
import random


class SumaLlevando:
    def __init__(self, adapter):
        self.adapter = adapter

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

    def get_carry_digits(self, numbers):
        
        # Invertir los números para empezar desde el dígito menos significativo
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

    def text_to_base64_audio(self, text, lang='es'):
        # Convertir texto a audio
        tts = gTTS(text=text, lang=lang)
        
        # Usar un archivo temporal para guardar el audio
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            tts.save(temp.name)
            temp.seek(0)
            audio = temp.read()
        
        # Convertir audio a base64
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        
        return audio_base64

    def generar_respuesta(self, student, message):
        num1, num2 = self.generate_example_numbers()
         
        numbers = [num1, num2]
        explanation_prompt = (
            f"Por favor '{student.name}' pregunto '{message}' , explica a  sobre la 'suma llevando'. "
            f"En ese caso usa estos numeros {numbers} para explicar este concepto. La explicación debe ser  para niños de 7 años, simple y divertida. Limita la respuesta a 150 palabras"
        )

        explanation_text = self.adapter.get_response_part(explanation_prompt, max_tokens=800)

       
        json_conversion_prompt = (
            f"Revisa que este texto tenga sentido y convierte la siguiente explicación en una estructura json: \n\n"
            f"'{explanation_text}'\n\n"
            f"La respuesta debe estar en el siguiente formato JSON:\n"
            f"{{\n"
            f"  'saludo': 'Texto de saludo a {student.name} o introducción breve',\n"
            f"  'tema': 'Descripción general del tema de suma llevando',\n"
            f"  'ejemplo': {{\n"
            f"    'problema': 'Problema o situación de suma llevando',\n"
            f"    'pasos': ['Primer paso o acción', 'Segundo paso o acción', '...'],\n"
            f"    'resultado': 'Resultado final de la suma llevando'\n"
            f"  }},\n"
            f"  'conclusion': 'Conclusión general sobre suma llevando',\n"
            f"  'sugerencia_practica': 'Sugerencias para practicar suma llevando'\n"
            f"}}\n"
        )

        explanation_json = self.adapter.get_response_part(json_conversion_prompt, max_tokens=800)


        result = sum(numbers)

        carry_digits = self.get_carry_digits(numbers)
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
