import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import initialize_firebase

from application.use_cases import SaveComplaintUseCase

from infrastructure.api import ChatGPTAdapter
from infrastructure.repositories.FirebaseComplaintRepository import FirebaseComplaintRepository
from infrastructure.exceptions.exception_handler import handle_exception

load_dotenv()

# Crea la aplicación Flask.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000","https://6531a66351505f0008c56dbd--neon-sunshine-53f478.netlify.app","https://master--neon-sunshine-53f478.netlify.app"], supports_credentials=True)

# Inicializa Firebase.
initialize_firebase()


firebaseComplaintRepository = FirebaseComplaintRepository()
chatGptAdapter = ChatGPTAdapter()

saveComplaintUseCase = SaveComplaintUseCase(firebaseComplaintRepository, chatGptAdapter)

@app.errorhandler(Exception)
def error_handler(e):
    logging.exception(handle_exception(e))
    return handle_exception(e)

@app.route('/complaint', methods=['POST'])
def save_complaint_endpoint():
    data = request.json

    saveComplaintUseCase.execute(data['complaint'])

    return "Proceso exitoso", 200
