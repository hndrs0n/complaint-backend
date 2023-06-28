import openai
import json
import os

class ChatGPTAdapter:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def generate_response(self, student, message):
        prompt = self.build_prompt(student, message)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=1300,  # Limitar el número de tokens puede acelerar la respuesta.
            temperature=0.1,  # Una temperatura más baja hace que la salida sea más determinista.
        )
        formatted_response = self.format_response(response.choices[0].message['content'])
        return formatted_response
    
    def build_prompt(self, student, message):
        
        prompt = (
            f"Estás asistiendo a {student.name}, un estudiante de segundo grado de primaria que "
            f"ha formulado la siguiente pregunta: \"{message['question']}\". Tu tarea es responder "
            f"de una manera creativa y práctica, como si fueras un maestro amigable. Intenta usar dibujos, "
            f"gestos con las manos u otras herramientas que pueda ser fácilmente comprendida "
            f"por un niño de segundo grado.\n"
            
            f"Tu respuesta debería contener una 'explicación' que presente un concepto de manera "
            f"general, utilizando un ejemplo diferente al problema propuesto y debe tener minimo 500 caracteres. Luego, proporciona un 'ejemplo' "
            f"separado con un 'problema' específico, 'alternativas', 'respuesta_incorrecta', 'solución' y "
            f"'explicacion_dinamica'. Asegúrate de que las 'alternativas' solo contengan números, no operaciones. "
            f"Y que la 'explicacion_dinamica', 'solución' y 'respuesta_incorrecta' expliquen el procedimiento y "
            f"motiven al estudiante, con al menos 250 caracteres cada uno.\n"
            
            f"Por favor, sigue la siguiente estructura JSON:\n"
            "{ \"explicacion\": \"\", \"ejemplo\": { \"problema\": \"\", \"alternativas\": "
            "[ { \"esCorrecta\": \"\", \"alternativa\": \"\" } ], \"respuesta_incorrecta\": \"\", "
            "\"solucion\": \"\", \"explicacion_dinamica\": \"\" } }"
        )
        return prompt

    def format_response(self, response_text):
        response_text = response_text.strip().replace('\\"', '"').replace('\\n', ' ')
        try:
            formatted_response = json.loads(response_text)
            return formatted_response
        except json.JSONDecodeError:
            print(f"Failed to decode JSON: {response_text}")
            return None
