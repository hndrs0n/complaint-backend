import openai

class SumaLlevando:
    def __init__(self, adapter):
        self.adapter = adapter

    def generar_respuesta(self, student, message):
        print (student)
        explanation_prompt = (
            f"Imagina que estás hablando con {student.name}, un niño de 7 años que está aprendiendo matemáticas. "
            f"Él te preguntó: '{message}'. Describe el concepto de 'sumas llevando' de una manera sencilla, "
            f"divertida y fácil de entender relacionada con su pregunta. "
            f"Podrías usar ejemplos cotidianos o situaciones con las que un niño podría relacionarse."
        )

        explanation = self.adapter.get_response_part(explanation_prompt)

        numbers_example = self.adapter.get_response_part(f"Proporciona dos números específicos para realizar una 'suma llevando', unicamente proporcioname los numeros y deben estar separados por espacios.")
        
        numbers = [int(num) for num in numbers_example.split() if num.strip().isdigit()]
        result = sum(numbers)


        # Construyendo y retornando la estructura JSON deseada
        return {
            "response": {
                "type": "sumaLlevando",
                "content": explanation,
                "data": {
                    "numbers": numbers,
                    "result": result
                }
            }
        }
