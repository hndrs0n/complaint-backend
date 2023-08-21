import openai
import os
import json

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def generate_response(self, student, message, response_type):
        
        prompts = self.build_prompts(student, message)
        
        response = {}
        previous_responses = ''

        # Only generate the requested response type
        if response_type in prompts:
            # Add previous responses to the prompt
            complete_prompt = prompts[response_type] + previous_responses
            print(complete_prompt)
            response[response_type] = self.get_response_part(complete_prompt)

        return response

    def get_response_part(self, prompt):
        openai_response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=500,
            temperature=0.3,
        )

        response_text = openai_response.choices[0].message['content'].strip()
        return response_text

    def build_prompts(self, student, question):
        prompts = {
            'explicacion': (
                f"Estás asistiendo a {student.name}, un estudiante de segundo grado de primaria que "
                f"ha formulado la siguiente pregunta: \"{question}\". Necesitas interpretar la pregunta y proporcionar una "
                f"explicación apropiada y detallada del concepto relacionado. Por favor, asegúrate de que tu explicación sea clara, "
                f"utilizando un lenguaje sencillo y amigable. Recuerda que tu audiencia es un estudiante de 7 años. "
                f"Además, intenta incluir ejemplos y métodos relevantes que puedan facilitar la comprensión del niño, "
                f"como utilizar dibujos o métodos de conteo cuando sea apropiado. "
                f"Finalmente, formatea la explicación con etiquetas HTML, sin incluir imagenes, para que la presentación sea más dinámica y atractiva para los niños.\n\n"
            ),
            'problema': (
                f"Ahora, genera un problema específico relacionado con el concepto \"{question}\" "
                f"para {student.name}. El problema debe ser relevante y apropiado para un estudiante de 7 anos.\n\n"
                f"Explicación anterior: "
            ),
            'alternativas': (
                f"Genial. Ahora, proporciona algunas alternativas de respuesta para el problema propuesto. "
                f"Incluye tanto la respuesta correcta como algunas respuestas incorrectas.\n\n"
                f"Problema propuesto: "
            ),
            'explicacion_dinamica': (
                f"Perfecto. Ahora, genera una explicación detallada y atractiva para resolver el problema propuesto. "
                f"Esta explicación debe ser comprensible para un estudiante de segundo grado.\n\n"
                f"Alternativas propuestas: "
            ),
            'respuesta_incorrecta': (
                f"Finalmente, genera un mensaje amigable y motivador en caso de que {student.name} elija una respuesta incorrecta. "
                f"La explicación dinámica fue: "
            ),
        }

        return prompts

