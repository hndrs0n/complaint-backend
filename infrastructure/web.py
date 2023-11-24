import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import initialize_firebase

from application.use_cases import SolveMathProblemWithExampleUseCase

from infrastructure.api import ChatGPTAdapter
from infrastructure.repositories.FirebaseQuestionRepository import FirebaseQuestionRepository
from infrastructure.exceptions.exception_handler import handle_exception

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Crea la aplicación Flask.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000","https://6531a66351505f0008c56dbd--neon-sunshine-53f478.netlify.app","https://master--neon-sunshine-53f478.netlify.app"], supports_credentials=True)

# Inicializa Firebase.
initialize_firebase()


questionRepository = FirebaseQuestionRepository()
chatGptAdapter = ChatGPTAdapter()
solveMathProblemWithExample = SolveMathProblemWithExampleUseCase(questionRepository, chatGptAdapter)

@app.errorhandler(Exception)
def error_handler(e):
    logging.exception(handle_exception(e))
    return handle_exception(e)

@app.route('/questions-with-example', methods=['POST'])
def solve_math_problem_with_example_endpoint():
    data = request.json

    response = solveMathProblemWithExample.execute(data['question'])

    return jsonify({'response': response}), 200
