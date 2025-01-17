import os
from flask import Blueprint, app, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
from controls.tda.asignacionControl import AsignacionControl
from controls.tda.cursoControl import CursoControl
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
from controls.tda.cursoControl import CursoControl
import json
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
    login, rol, cursos, tiene, nombreRol, nombre, apellido = cc.iniciarSesion(data["correo"], data["contrasenia"]) #Aqui llamo al metodo del controlador cc
    print("##################dasdsd################3")
    print(login)
    print(rol)
    cursos.print
    print(tiene)
    
    if login == -1:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('router.inicio'))
    elif login == 0:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('router.inicio'))
    else:
        if rol == "Administrador":
            return render_template('administrador/administrador.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = nombre, apellidoU = apellido)
        elif rol == "Docente":
            return render_template('docente/docenteInicio.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = nombre, apellidoU = apellido)
        elif rol == "Estudiante":
            return render_template('estudiante/inicioEstudiante.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = nombre, apellidoU = apellido)
        
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
    
    return render_template(
        '/estudiante/estudianteInicio.html', 
        roles=nombreRol._nombre, 
        nombreU=nombreU._nombre, 
        apellidoU=apellidoU._apellido
    )


@router.route('/estudiante/curso/tareas')
def tareas():
    control = AsignacionControl()
    asignaciones = control.obtener_asignaciones()
    return render_template('/estudiante/curso/tareas.html', asignaciones=asignaciones)



@router.route('/estudiante/subir_tarea')
def subir_tarea():
    return render_template('/estudiante/curso/subirTarea.html')

@router.route('/estudiante/inicioTest')
def testInicio():
    return render_template('/estudiante/testsE/inicioTest.html')

@router.route('/estudiante/tests/ver')
def verTests():
    return render_template('/estudiante/testsE/test.html')



@router.route('/estudiante/inicioEstudiante', methods=['GET'])
def inicioEstudiante():
    return render_template('/estudiante/inicioEstudiante.html')

@router.route('/estudiante/perfil', methods=['GET'])
def perfil():
    return render_template('/estudiante/perfil.html')

@router.route('/logout')
def logout():
    return render_template("inicio.html")

@router.route('/estudiante/asignarEstudiante', methods=['POST'])
def asignarEstudiante():
    estudiantes_seleccionados = request.form.getlist('estudiantes')
    
    print("cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
    print(estudiantes_seleccionados)
    
    return render_template('/administrador/asignarCurso.html')



#------------ Vista Docente------------------------#
@router.route('/docente')
def docente():
    return render_template('/docente/docente.html')


@router.route('/docenteInicio', methods=['GET'])
def docenteInicio():
    return render_template('/docente/docenteCursos.html')


@router.route('/docente/crearAsignacion/<cursos>', methods=['GET'])
def crearTarea(cursos):
    cursos_lista = eval(cursos)
    ec = EstudianteControl()
    estudiantes = ec._list()
    estudiantes = estudiantes.toArray
    listaEst = Linked_List()
    for curso in cursos_lista:
        if curso["nombre"] != "Sin cursos":
            for estudia in estudiantes:
                if estudia._idCurso == curso["id"]:
                    listaEst.addNode(estudia)
                    
                    
    
    print("$$$$$$$$$$$$$$$$$$$$$$4")
    listaEst.print
    
    arrayEst = listaEst.toArray
    uc= UsuarioControl()
    usuarios = uc._list()
    lista = Linked_List()
    
    for est in arrayEst:
        usuario = usuarios.binary_search_models(est._idUsuario, "_id")
        if usuario != -1:
            lista.addNode(usuario)
    
    lista.print
    return render_template('/docente/crearAsignacion.html', cursos = cursos_lista, estudiantes = ec.to_dic_lista(listaEst), usuarios = uc.to_dic_lista(lista))

# @router.route('/docente/eliminarAsignados', methods=['GET'])
# def eliminarAsignados():
#     return render_template('/docente/eliminarAsignados.html')

# @router.route('/docente/evaluacionEstres', methods=['GET'])
# def evaluacionEstres():
#     return render_template('/docente/evaluacionEstres.html')

# @router.route('/docente/gestionGeneral', methods=['GET'])
# def gestionGeneral():
#     return render_template('/docente/gestionGeneral.html')

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

@router.route('/administrador/crearCurso')
def crearCurso():
    return render_template('administrador/crearCurso.html')

@router.route('/administrador/crearCursoPost', methods=['POST'])
def crearCursoPost():
    data = request.form
    cc = CursoControl()
    cc.crearCurso(data["nombre"], data["paralelo"], data["idDocente"])
    flash('Curso creado con exito', 'success')
    return redirect(url_for('router.administrador'))

@router.route('/administrador/asignarCurso')
def asignarCurso():
    cc = CursoControl()
    cursos = cc._list()
    ec = EstudianteControl()
    estudiantes = ec._list()
    
    estArray = estudiantes.toArray 
    uc = UsuarioControl()
    usuarios = uc._list()
    lista = Linked_List()
    
    for est in estArray:
        usuario = usuarios.binary_search_models(est._idUsuario, "_id")
        if usuario != -1:
            lista.addNode(usuario)
    
    return render_template('administrador/asignarCurso.html', cursos = cc.to_dic_lista(cursos), estudiantes = ec.to_dic_lista(lista))

