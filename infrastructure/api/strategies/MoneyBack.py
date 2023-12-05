
class MoneyBack:
    def __init__(self, adapter):
        self.adapter = adapter


    def generar_respuesta(self, message):

        explanation_prompt = (
            f"Considera que eres el encargado de responder los reclamos de una tienda de mejoramiento de hogar del Peru,"
            f" debes de responder al cliente, como le responderias si este fuera el reclamo: '{message}'"
        )

        answer = self.adapter.get_response_part(explanation_prompt, max_tokens=800)

        return answer