import base64
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from gtts.lang import tts_langs


class SumaLlevando:
    def __init__(self, adapter):
        self.adapter = adapter

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
            f"¡Hola {student.name}! Vamos a hablar sobre la 'suma llevando'. Es una técnica que usamos cuando sumamos dos números y uno de los dígitos de la suma supera el 9. "
            f"En ese caso, 'llevamos' 1 al siguiente dígito. Por favor, explica el proceso paso a paso de manera simple y divertida. "
            f"La respuesta no debe tener más de 100 palabras."
        )

        explanation = self.adapter.get_response_part(explanation_prompt, max_tokens=500)


        numbers_example = self.adapter.get_response_part(f"Proporciona dos números específicos para realizar una 'suma llevando', unicamente proporcioname los numeros y deben estar separados por espacios.")
        
        numbers = [int(num) for num in numbers_example.split() if num.strip().isdigit()]

        narration_prompt = f"Por favor, narra paso a paso cómo sumar los números {numbers[0]} y {numbers[1]} utilizando la técnica de 'suma llevando'. Solo pon los pasos narrados para un nino de 7 anos"
        narration = self.adapter.get_response_part(narration_prompt, max_tokens=300)
        text = "hola como estas"
        tts = gTTS(text=text, lang='es')
        print(tts)
        narration_audio_base64 = self.text_to_base64_audio("Hola, ¿cómo estás?")
        result = sum(numbers)

        carry_digits = self.get_carry_digits(numbers)

        # Construyendo y retornando la estructura JSON deseada
        return {
            "response": {
                "type": "sumaLlevando",
                "content": explanation,
                "data": {
                    "numbers": numbers,
                    "result": result,
                    "carry_digits": carry_digits,
                    "narration": narration,
                    "narration_audio": narration_audio_base64
                }
            }
        }
