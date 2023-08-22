import openai
import os
from .strategies import EstrategiaBase, SumaLlevando  # Importar las estrategias necesarias

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.estrategias = {
            "sumas llevando": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "restas prestando": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "comparación de números": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "problemas de sumas y retas": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "anterior y posterior": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "descomposición de números": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "patrones numéricos": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "operaciones combinadas de sumas y restas": SumaLlevando(self)
        }

    def generate_response(self, student, message):
        # Determinar el tema usando GPT-3
        topic = self.determine_topic(message)
        
        # Buscar la estrategia correspondiente y generar la respuesta
        estrategia = self.estrategias.get(topic)
        if estrategia:
            return estrategia.generar_respuesta(student, message)
        
        # En caso de que no se encuentre una estrategia, devolvemos un mensaje genérico
        return {
            "response": {
                "type": "unknown",
                "content": "Lo siento, no pude determinar el tema de tu pregunta.",
                "data": {}
            }
        }

    def determine_topic(self, message):
        topics_list = ", ".join(self.estrategias.keys())
        topic_prompt = f"Basándote en la pregunta '{message}', ¿cuál de los siguientes temas es el más adecuado? Opciones: {topics_list}. Tu respuesta solo debe contener una de estas opciones, no agregues mas palabras solo nombre la opcion que corresponde."
        response = self.get_response_part(topic_prompt)

        return response.lower()

    def get_response_part(self, prompt, max_tokens=500):
        
        openai_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=[
                {'role': 'system', 'content': 'You are a math teacher for children.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.1,
        )
        
        response_text = openai_response.choices[0].message['content'].strip()
        
        return response_text
