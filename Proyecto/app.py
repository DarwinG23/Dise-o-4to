from flask import Flask
from flask_login import LoginManager
from controls.tda.usuarioControl import UsuarioControl
from flask_login import LoginManager, current_user
from flask import Flask, redirect, url_for, request
import os
def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.config.Config')
    app.secret_key = 'pis123'
    
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "router.inicio"
    

    
    # Este es el decorador user_loader que Flask-Login usa
    @login_manager.user_loader
    def load_user(usuario_id):
        uc = UsuarioControl()  # Controlador que accede a los datos de los usuarios
        usuario = uc._list().binary_search_models(usuario_id, "_id")  # Método para obtener el usuario por su ID
        if usuario != -1:
            # Crear una instancia de Usuario
            user = usuario
            return user
        else:
            return None

    
    # Crear la carpeta de subida si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    with app.app_context():
        #from routes.api import api
        #app.register_blueprint(api)
        from routes.router import router
        app.register_blueprint(router)
    return app


    