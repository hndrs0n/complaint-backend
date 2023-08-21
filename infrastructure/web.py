
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

from application.use_cases import RegisterStudentUseCase, UpdateLearningContextUseCase, AddInteractionUseCase, SolveMathProblemUseCase
from infrastructure.repositories.student_repository import FirebaseStudentRepository
from infrastructure.api import ChatGPTAdapter
from config import initialize_firebase

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Crea la aplicación Flask.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Inicializa Firebase.
initialize_firebase()

# Instancia los casos de uso.

# Recupera la clave de la API de las variables de entorno y crea el adaptador.


student_repository = FirebaseStudentRepository()
register_student = RegisterStudentUseCase(student_repository)
update_learning_context = UpdateLearningContextUseCase(student_repository)
add_interaction = AddInteractionUseCase(student_repository)
chat_gpt_adapter = ChatGPTAdapter()
solve_math_problem = SolveMathProblemUseCase(student_repository, chat_gpt_adapter)


@app.route('/students/<id>/solve', methods=['POST'])
def solve_math_problem_endpoint(id):
    data = request.json
    response = solve_math_problem.execute(id, data['question'])
    print(response)
    return jsonify({'response': response}), 200
