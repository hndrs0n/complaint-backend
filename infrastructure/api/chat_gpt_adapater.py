import openai
import os
from .strategies import SumaLlevando, RestasPrestando, ComparacionNumeros, AnteriorPosterior

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.estrategias = {
            "sumas llevando": SumaLlevando(self),
            "restas prestando": RestasPrestando(self),
            "comparación de números": ComparacionNumeros(self),
            "problemas de sumas y retas": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "anterior y posterior": AnteriorPosterior(self),
            "descomposición de números": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "patrones numéricos": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "operaciones combinadas de sumas y restas": SumaLlevando(self)
        }

    def generate_response(self, message):

        topic = self.determine_topic(message)
        print("El tema identificado es este: " + topic)
        estrategia = self.estrategias.get(topic)
        if estrategia:
            return estrategia.generar_respuesta(message)

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
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': 'You are a math teacher for children.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.1,
        )
        
        response_text = openai_response.choices[0].message['content'].strip()
        
        return response_text
