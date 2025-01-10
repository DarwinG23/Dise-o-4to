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
@router.route('/estudiante', methods=['GET'])
def estudiante():
    return render_template('/estudiante/estudiante.html')

@router.route('/estudiante/inicioEstudiante', methods=['GET'])
def inicioEstudiante():
    return render_template('/estudiante/inicioEstudiante.html')

@router.route('/estudiante/perfil', methods=['GET'])
def perfil():
    return render_template('/estudiante/perfil.html')

#------------ Vista Docente-----------------#


@router.route('/docente/docenteInicio', methods=['GET'])
def docenteInicio():
    return render_template('/docente/docenteInicio.html')

@router.route('/docente/crearTarea', methods=['GET'])
def crearTarea():
    return render_template('/docente/crearTarea.html')

@router.route('/docente/eliminarAsignados', methods=['GET'])
def eliminarAsignados():
    return render_template('/docente/eliminarAsignados.html')

@router.route('/docente/evaluacionEstres', methods=['GET'])
def evaluacionEstres():
    return render_template('/docente/evaluacionEstres.html')

@router.route('/docente/gestionGeneral', methods=['GET'])
def gestionGeneral():
    return render_template('/docente/gestionGeneral.html')

#---------------------------------------------Administrador-----------------------------------------------------#
@router.route('/administrador', methods=['GET'])
def administrador():
    return render_template('administrador/administrador.html')

@router.route('/administrador/gestionar_usuarios', methods=['GET'])
def gestionar_usuarios():
    return render_template('administrador/gestionar_usuarios.html')

@router.route('/administrador/gestionar_tecnicas', methods=['GET'])
def gestionar_tecnicas():
    return render_template('administrador/gestionar_tecnicas.html')

@router.route('/administrador/configurar_alertas', methods=['GET'])
def configurar_alertas():
    return render_template('administrador/configurar_alertas.html')

@router.route('/administrador/visualizar_datos', methods=['GET'])
def visualizar_datos():
    return render_template('administrador/visualizar_datos.html')



