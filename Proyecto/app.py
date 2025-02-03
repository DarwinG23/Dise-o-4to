from flask import Flask
import os
def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.config.Config')
    app.secret_key = 'pis123'
    
    # Crear la carpeta de subida si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    with app.app_context():
        #from routes.api import api
        #app.register_blueprint(api)
        from routes.router import router
        app.register_blueprint(router)
    return app