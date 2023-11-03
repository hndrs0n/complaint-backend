import traceback
from flask import jsonify

def handle_exception(e):
    # Obtén el traceback como una cadena de texto
    tb_str = traceback.format_exc()

    response = {
        "error": str(e),
        "type": type(e).__name__,
        "traceback": tb_str  # Incluye el traceback en la respuesta
    }
    return jsonify(response), 500
