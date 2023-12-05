import firebase_admin
from firebase_admin import credentials
import os

def initialize_firebase():
    # Obtén la ruta absoluta del directorio del proyecto
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Crea la ruta al archivo de credenciales
    cred_path = os.path.join(project_dir, 'reclamos-c2d50-firebase-adminsdk-g8lpj-b616165607.json')

    # Usa esta ruta al inicializar la aplicación de Firebase
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://reclamos-c2d50-default-rtdb.firebaseio.com/'
    })