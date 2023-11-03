import openai
import os
from .strategies import EstrategiaBase, SumaLlevando, RestasPrestando  # Importar las estrategias necesarias


class ChatGPTAdapterGeneric:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.estrategias = {
            "sumas llevando": SumaLlevando(self),
            "restas prestando": RestasPrestando(self),
            "comparación de números": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "problemas de sumas y retas": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "anterior y posterior": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "descomposición de números": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "patrones numéricos": SumaLlevando(self),  # Pasamos la instancia actual del Adapter a la estrategia
            "operaciones combinadas de sumas y restas": SumaLlevando(self)
        }

    def generate_response(self, message):
        topic = self.determine_topic(message)
        print("El tema identificado es este: " + topic)
        topics_list = ", ".join(self.estrategias.keys())
        if topic not in topics_list:
            prompt = self.generate_promt_other_topic(message)
        else:
            prompt = self.generate_promt(message)
        response = self.get_response_part(prompt)

        return response.lower()

    def determine_topic(self, message):
        topics_list = ", ".join(self.estrategias.keys())
        topic_prompt = (f"Basándote en la pregunta '{message}', "
                        f"¿cuál de los siguientes temas es el más adecuado? Opciones: {topics_list}. "
                        f"Tu respuesta solo debe contener una de estas opciones, "
                        f"no agregues mas palabras solo nombre la opcion que corresponde."
                        f"Si no sabes que tema es, solo escribe 'ninguno'")
        response = self.get_response_part(topic_prompt)

        return response.lower()

    def generate_promt(self, message):
        return (f"Un nino de segundo grado de primaria consulta lo siguiente: '{message}'."
                f"Responde de manera que le resulte facil de entender, recuerda que tiene 7 anos y esta en segundo grado de primaria."
                f"La respuesta la incluire dentro de un componente de react, por favor formateala para que se vea bien, con salto de linea y bien formateado."
                f"Solo incluye etiquetas html y la respuesta, no agregues ningun mensaje adicional.")

    def generate_promt_other_topic(self, message):
        topics_list = ", ".join(self.estrategias.keys())
        return (f"Un nino de segundo grado de primaria consulta lo siguiente: '{message}'."
                f"Tu eres un asesor de mateticas de segundo grado de primaria y como la pregunta no tiene que ver con matematicas, "
                f"Dale una respuesta breve y sencilla, pero recuerdale que tu especialidad es cualquiera de estos temas: {topics_list}.")

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
