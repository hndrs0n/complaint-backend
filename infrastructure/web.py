
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import initialize_firebase

from application.use_cases import SolveMathProblemWithExampleUseCase, SolveMathProblemUseCase

from infrastructure.api import ChatGPTAdapterGeneric, ChatGPTAdapter
from infrastructure.repositories.FirebaseStudentRepository import FirebaseStudentRepository
from infrastructure.repositories.FirebaseQuestionRepository import FirebaseQuestionRepository

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Crea la aplicación Flask.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000","https://6531a66351505f0008c56dbd--neon-sunshine-53f478.netlify.app"], supports_credentials=True)

# Inicializa Firebase.
initialize_firebase()

studentRepository = FirebaseStudentRepository()
questionRepository = FirebaseQuestionRepository()
chatGptAdapter = ChatGPTAdapter()
chatGptAdapterGeneric = ChatGPTAdapterGeneric()
solveMathProblemWithExample = SolveMathProblemWithExampleUseCase(questionRepository, chatGptAdapter)
solveMathProblem = SolveMathProblemUseCase(questionRepository, chatGptAdapterGeneric)


@app.route('/students/<id>/solve', methods=['POST'])
def solve_math_problem_with_example_endpoint(id):
    data = request.json
    response = solveMathProblemWithExample.execute(data['question'])
    return jsonify({'response': response}), 200


@app.route('/questions', methods=['POST'])
def solve_math_problem_endpoint():
    data = request.json
    response = solveMathProblem.execute(data['question'])
    return jsonify({'response': response}), 200