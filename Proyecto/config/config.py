from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname('__file__'))
load_dotenv(path.join(base_dir, 'config/.env'))

class Config:
    #Configuracion general
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    # Configuración para los archivos
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER', 'uploads')  # Valor predeterminado: 'uploads'
    ALLOWED_EXTENSIONS = environ.get('ALLOWED_EXTENSIONS', 'pdf').split(',')  # Convertirlo a lista
    MAX_CONTENT_LENGTH = int(environ.get('MAX_CONTENT_LENGTH', 16)) * 1024 * 1024  # Convertir MB a bytes