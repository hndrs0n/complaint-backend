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
       
        explanation_prompt = (
            f"Por favor, explica a {student.name} sobre la 'suma llevando o suma con transformación' para niños de 7 años. Es una técnica que usamos cuando sumamos dos números y uno de los dígitos de la suma supera el 9. "
            f"En ese caso, 'llevamos' 1 al siguiente dígito. La explicación debe ser simple y divertida. Limita la respuesta a 100 palabras"
        )

        explanation_text = self.adapter.get_response_part(explanation_prompt, max_tokens=500)

       
        json_conversion_prompt = (
            f"Convierte la siguiente explicación en una estructura json: \n\n"
            f"'{explanation_text}'\n\n"
            f"La respuesta debe estar en el siguiente formato JSON:\n"
            f"{{\n"
            f"  'saludo': 'Texto de saludo a {student.name} o introducción breve',\n"
            f"  'tema': 'Descripción general del tema de suma llevando',\n"
            f"  'ejemplo': {{\n"
            f"    'problema': 'Problema o situación de suma llevando',\n"
            f"    'pasos': ['Primer paso o acción', 'Segundo paso o acción', '...'],\n"
            f"    'observaciones': ['Comentario o nota sobre el proceso', '...'],\n"
            f"    'resultado': 'Resultado final de la suma llevando'\n"
            f"  }},\n"
            f"  'analogia': 'Analogía o metáfora sobre suma llevando',\n"
            f"  'conclusion': 'Conclusión general sobre suma llevando',\n"
            f"  'sugerencia_practica': 'Sugerencias para practicar suma llevando'\n"
            f"}}\n"
        )

        explanation_json = self.adapter.get_response_part(json_conversion_prompt, max_tokens=800)

        num1, num2 = self.generate_example_numbers()
         
        numbers = [num1, num2]
        print(numbers)

        narration_prompt = f"Por favor, narra paso a paso cómo sumar los números {numbers[0]} y {numbers[1]} utilizando la técnica de 'suma llevando'. Solo pon los pasos narrados para un nino de 7 anos"
        narration = self.adapter.get_response_part(narration_prompt, max_tokens=300)
        #text = "hola como estas"
        #tts = gTTS(text=text, lang='es')
        #print(tts)
        #narration_audio_base64 = self.text_to_base64_audio("Hola, ¿cómo estás?")
        result = sum(numbers)

        carry_digits = self.get_carry_digits(numbers)

        # Construyendo y retornando la estructura JSON deseada
        return {
            "response": {
                "type": "sumaLlevando",
                "content": explanation_json,
                "data": {
                    "numbers": numbers,
                    "result": result,
                    "carry_digits": carry_digits,
                    "narration": narration,
                    #"narration_audio": narration_audio_base64
                }
            }
        }
