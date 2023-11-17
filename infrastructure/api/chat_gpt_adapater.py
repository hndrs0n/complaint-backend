import openai
import os
from .strategies import SumaLlevando, RestasPrestando, ComparacionNumeros, AnteriorPosterior, DescomposicionNumeros, PatronesNumericos

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.estrategias = {
            "sumas llevando": SumaLlevando(self),
            "restas prestando": RestasPrestando(self),
            "comparación de números": ComparacionNumeros(self),
            "anterior y posterior": AnteriorPosterior(self),
            "descomposición de números": DescomposicionNumeros(self),
            "patrones numéricos": PatronesNumericos(self),
            "operaciones combinadas de sumas y restas": SumaLlevando(self)
        }

    def generate_response(self, message):

        topic = self.determine_topic(message)
        estrategia = self.estrategias.get(topic)
        if estrategia:
            return estrategia.generar_respuesta(message)

        prompt = self.generate_promt_other_topic(message)
        return self.get_response_part(prompt)


    def generate_promt_other_topic(self, message):
        topics_list = ", ".join(self.estrategias.keys())
        return (f"Un nino de segundo grado de primaria consulta lo siguiente: '{message}'."
                f"Tu eres un asesor de mateticas de segundo grado de primaria llamado Smart tutor, como la pregunta no tiene que ver con matematicas, "
                f"Indica que no puedes responder y recuerdale que tu especialidad es cualquiera de estos temas: {topics_list}.")

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
