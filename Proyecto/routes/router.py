from flask import Blueprint, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
from controls.util.read import Read
from io import BytesIO
from controls.util.cedula import Cedula
router = Blueprint('router', __name__)




#CORS(api)2
cors = CORS(router, resource={
    r"/*":{
        "origins":"*"
    }
})

#GET: PARA PRESENTAR DATOS
#POST: GUARDA DATOS, MODIFICA DATOS Y EL INICIO DE SESION, EVIAR DATOS AL SERVIDOR

#---------------------------------------------Login-----------------------------------------------------#
@router.route('/', ) #SON GETS
def inicio():
    return render_template('inicio.html')


#------------ Vista Estudiante-----------------#
@router.route('/estudiante')
def estudiante():
    return render_template('/estudiante/estudiante.html')



#------------ Vista Docente-----------------#
@router.route('/docente')
def docente():
    return render_template('/docente/docente.html')


@router.route('/administrador')
def administrador():
    return render_template('administrador/administrador.html')  # Asegúrate de que esta ruta sea correcta

# Página para gestionar usuarios
@router.route('/administrador/gestionar_usuarios')
def gestionar_usuarios():
    return render_template('administrador/gestionar_usuarios.html')

# Página para gestionar técnicas de reducción de estrés
@router.route('/administrador/gestionar_tecnicas')
def gestionar_tecnicas():
    return render_template('administrador/gestionar_tecnicas.html')

# Página para configurar alertas
@router.route('/administrador/configurar_alertas')
def configurar_alertas():
    return render_template('administrador/configurar_alertas.html')

# Página para visualizar datos generales
@router.route('/administrador/visualizar_datos')
def visualizar_datos():
    return render_template('administrador/visualizar_datos.html')


@router.route('/estudiante/inicioEstudiante')
def inicioEstudiante():
    return render_template('/estudiante/inicioEstudiante.html')