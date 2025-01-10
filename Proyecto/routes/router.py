from flask import Blueprint, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
from controls.util.read import Read
from io import BytesIO
from controls.util.cedula import Cedula
from controls.tda.cuentaControl import CuentaControl
from controls.tda.usuarioControl import UsuarioControl
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

@router.route('/login',  methods=["POST"])
def login():
    data = request.form
    cc = CuentaControl()
    cuenta = cc._list().binary_search_models(data["correo"], "_correo")
    if cuenta == -1:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('router.inicio'))
    elif cuenta._contrasena == data["contrasenia"]:
        #uc = UsuarioControl()
        #listaUsuarios = uc._list()
        #usuario = listaUsuarios.binary_search_models(cuenta._idUsuario, "_id")
        roles = cuenta._roles
        roles.print
        admin = roles.binary_search_models("Administrador", "_nombre")
        docente = roles.binary_search_models("Docente", "_nombre")
        estudiante = roles.binary_search_models("Estudiante", "_nombre")
        
        if admin != -1:
            return render_template('administrador/administrador.html')
        elif docente != -1:
            return render_template('docente/docente.html')
        elif estudiante != -1:
            return render_template('estudiante/inicioEstudiante.html')
    else:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('router.inicio'))
#---------------------------------------------Presentación-----------------------------------------------#
@router.route('/presentacion') 
def presentacion():
    return render_template('/presentacion/presentacion.html')
#------------ Vista Estudiante--------------------#
@router.route('/estudiante')
def estudiante():
    return render_template('/estudiante/estudiante.html')

@router.route('/logout')
def logout():
    return render_template(url_for('/'))

@router.route('/estudiante/inicioEstudiante', methods=['GET'])
def inicioEstudiante():
    return render_template('/estudiante/inicioEstudiante.html')

@router.route('/estudiante/perfil', methods=['GET'])
def perfil():
    return render_template('/estudiante/perfil.html')

#------------ Vista Docente------------------------#
@router.route('/docente')
def docente():
    return render_template('/docente/docente.html')


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



