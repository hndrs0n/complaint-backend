import openai
import os
from .strategies import MoneyBack, Change, Other

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.estrategias = {
            "devolucion de dinero": MoneyBack(self),
            "cambio de producto": Change(self),
            "otros": Other(self)
        }

    def generate_response(self, message, topic):

        if not topic:
            return self.determine_topic(message)

        estrategia = self.estrategias.get(topic)

        return estrategia.generar_respuesta(message)

    def determine_topic(self, message):
        topics_list = ", ".join(self.estrategias.keys())
        topic_prompt = (f"Basandote en el siguiente reclamo: '{message}', responde ¿cuál de los siguientes temas es el más adecuado? Opciones: {topics_list}. Tu respuesta solo debe contener una de estas opciones, no agregues mas palabras solo nombre la opcion que corresponde.")
        response = self.get_response_part(topic_prompt)

        return response.lower()

    def get_response_part(self, prompt, max_tokens=500):
        
        openai_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are the customer service manager in a department store'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.1,
        )
        
        response_text = openai_response.choices[0].message['content'].strip()
        
        return response_text
