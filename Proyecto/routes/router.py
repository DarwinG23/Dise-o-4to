from flask import Blueprint, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
from controls.util.read import Read
from io import BytesIO
from controls.util.cedula import Cedula
from controls.tda.cuentaControl import CuentaControl
from controls.tda.usuarioControl import UsuarioControl
from controls.tda.rolContol import RolControl
from controls.tda.linked.linkedList import Linked_List
from controls.tda.estudianteControl import EstudianteControl
from controls.tda.docenteControl import DocenteControl
from controls.tda.administradorControl import AdministradorControl
from datetime import datetime
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
    login, rol = cc.iniciarSesion(data["correo"], data["contrasenia"]) #Aqui llamo al metodo del controlador cc
    if login == -1:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('router.inicio'))
    elif login == 0:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('router.inicio'))
    else:
        if rol == "Administrador":
            return render_template('administrador/administrador.html')
        elif rol == "Docente":
            return render_template('docente/docenteInicio.html')
        elif rol == "Estudiante":
            return render_template('estudiante/inicioEstudiante.html')
        
@router.route('/registrarEstudiante')
def registrarEstudiante():
    return render_template('registro.html',usuario = "Estudiante")   

@router.route('/registrarDocente')
def registrarDocente():
    return render_template('registro.html',usuario = "Docente")

@router.route('/registrarAdministrador')
def registrarAdministrador():
    return render_template('registro.html',usuario = "Administrador") 
        
@router.route('/registro/<rol>', methods=["POST"])
def registro(rol):
    data = request.form
    uc = UsuarioControl()
    cc = CuentaControl()
    rc = RolControl()
    # Convertir la cadena a un objeto datetime
    fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
    fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
    fecha_formateada = str(fecha_formateada)

    uc.crearUsuario(data["nombre"],data["apellido"], data['ci'], fecha_formateada, data['telefono'], data['direccion'])
    usuario = uc._list().getData(uc._list()._length-1)
    cc.crearCuenta(data['correo'], data['contrasenia'], usuario._id)
    cuenta = cc._list().getData(cc._list()._length-1)
    rc.crearRol(rol, cuenta._id)
    
    if rol == "Estudiante":
        ec = EstudianteControl()
        ec.agregarDatos(data["matricula"], data["contacto"], usuario._id)
    elif rol == "Docente":
        dc = DocenteControl()
        dc.agregarTitulo(data["titulo"],  usuario._id)
    elif rol == "Administrador":
        ac = AdministradorControl()
        ac.agregarDatos(usuario._id)
        
    flash('Cuenta creada con exito', 'success')
    return redirect(url_for('router.inicio'))
#---------------------------------------------Presentación-----------------------------------------------#
@router.route('/presentacion') 
def presentacion():
    return render_template('/presentacion/presentacion.html')



#------------ Vista Estudiante--------------------#
@router.route('/estudiante')
def estudiante():
    rc = RolControl()
    uc = UsuarioControl()
    rol = rc._list()
    usuario = uc._list()
    nombreRol = rol.binary_search_models("Estudiante", "_nombre")
    nombreU = usuario.binary_search_models(1, "_id")
    apellidoU = usuario.binary_search_models(1, "_id")
    return render_template('/estudiante/estudianteInicio.html', roles = nombreRol._nombre, nombreU = nombreU._nombre, apellidoU = apellidoU._apellido)




@router.route('/estudiante/inicioTest')
def testInicio():
    return render_template('/estudiante/testsE/inicioTest.html')

@router.route('/estudiante/tests/ver')
def verTests():
    return render_template('/estudiante/testsE/test.html')

@router.route('/estudiante/curso/tareas')
def tareas():
    return render_template('/estudiante/curso/tareas.html')

@router.route('/estudiante/inicioEstudiante', methods=['GET'])
def inicioEstudiante():
    return render_template('/estudiante/inicioEstudiante.html')

@router.route('/estudiante/perfil', methods=['GET'])
def perfil():
    return render_template('/estudiante/perfil.html')

@router.route('/logout')
def logout():
    return render_template("inicio.html")



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



