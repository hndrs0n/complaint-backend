import openai
import os
from .strategies import EstrategiaBase, SumaLlevando, RestasPrestando  # Importar las estrategias necesarias


class ChatGPTAdapterGeneric:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def generate_response(self, message):
        prompt = self.generate_promt(message)
        response = self.get_response_part(prompt)

        return response.lower()

    def generate_promt(self, message):
        return (f"Un nino de segundo grado de primaria consulta lo siguiente: '{message}'."
                f"Responde de manera que le resulte facil de entender, recuerda que tiene 7 anos y esta en segundo grado de primaria."
                f"La respuesta la incluire dentro de un componente de react, por favor formateala para que se vea bien, con salto de linea y bien formateado."
                f"Solo incluye etiquetas html y la respuesta, no agregues ningun mensaje adicional.")

    def get_response_part(self, prompt, max_tokens=1000):
        openai_response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': 'You are a math teacher for children.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.5,
        )

        response_text = openai_response.choices[0].message['content'].strip()

        return response_text
