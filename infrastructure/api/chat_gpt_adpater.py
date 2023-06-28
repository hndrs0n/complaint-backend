import openai
import os
import json

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def generate_response(self, student, message):
        prompts = self.build_prompts(student, message)
        response = {}
        previous_responses = ''

        for part, prompt in prompts.items():
            # Add previous responses to the prompt
            complete_prompt = prompt + previous_responses
            response[part] = self.get_response_part(complete_prompt)
            # Add this response to previous responses
            previous_responses += ' ' + response[part]

        return response

    def get_response_part(self, prompt):
        openai_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=200,
            temperature=0.3,
        )

        response_text = openai_response.choices[0].message['content'].strip()
        return response_text

    def build_prompts(self, student, message):
        prompts = {
            'explicacion': (
                f"Estás asistiendo a {student.name}, un estudiante de segundo grado de primaria que "
                f"ha formulado la siguiente pregunta: \"{message['question']}\". Por favor, proporciona una "
                f"explicación del concepto general de manera clara y fácil de entender para un niño de segundo grado."
            ),
            'problema': (
                f"Ahora, por favor genera un problema específico relacionado con el concepto que el estudiante "
                f"{student.name} preguntó, \"{message['question']}\". Recuerda, el problema debe ser relevante "
                f"y apropiado para un estudiante de segundo grado. La explicación anterior fue: "
            ),
            'alternativas': (
                f"Genial. Ahora, por favor genera algunas alternativas de respuesta para el problema que has propuesto. "
                f"Incluye tanto la respuesta correcta como algunas respuestas incorrectas. El problema propuesto fue: "
            ),
            'explicacion_dinamica': (
                f"Perfecto. Ahora, por favor genera una explicación dinámica para el problema que has propuesto. "
                f"Esta debe ser una explicación detallada del procedimiento para resolver el problema, con un enfoque en "
                f"hacerlo atractivo y comprensible para un estudiante de segundo grado. Las alternativas propuestas fueron: "
            ),
            'respuesta_incorrecta': (
                f"Finalmente, por favor genera un mensaje amigable y motivador que el asistente puede dar al estudiante "
                f"{student.name} en caso de que él o ella elijan una respuesta incorrecta al problema propuesto. La explicación dinámica fue: "
            ),
        }

        return prompts
