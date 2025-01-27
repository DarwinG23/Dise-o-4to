import os
from flask import Blueprint, app, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
from controls.tda.asignacionControl import AsignacionControl
from controls.tda.cursoControl import CursoControl
from controls.tda.permisoControl import PermisoControl
from controls.tda.preguntaControl import PreguntaControl
from controls.tda.testControl import TestControl
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
    legth = uc._list()._length
    cc.crearCuenta(data['correo'], data['contrasenia'], legth) 
    cuenta = cc._list().getData(cc._list()._length-1)
    rc.crearRol(rol, cuenta._id)
    
    if rol == "Estudiante":
        ec = EstudianteControl()
        ec.agregarDatos(data["matricula"], data["contacto"], legth)
    elif rol == "Docente":
        dc = DocenteControl()
        dc.agregarTitulo(data["titulo"],  legth)
    elif rol == "Administrador":
        ac = AdministradorControl()
        ac.agregarDatos(legth)
        
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
                    
                    

    
    arrayEst = listaEst.toArray
    uc= UsuarioControl()
    usuarios = uc._list()
    lista = Linked_List()
    
    for est in arrayEst:
        usuario = usuarios.binary_search_models(est._idUsuario, "_id")
        if usuario != -1:
            lista.addNode(usuario)
    

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

#################################################################################################################
#Presentar la lista de usuarios
@router.route('/administrador/gestionar_usuarios', methods=['GET'])
def gestionar_usuarios():
    uc = UsuarioControl() #Creo un objeto de la clase UsuarioControl
    listaUsuarios = uc._list() #Obtengo la lista de usuarios
    listaUsuarios.sort_models("_id",1,4) #La ordeno por id para presentarla
    return render_template('administrador/crud/listaUsuario.html', lista = uc.to_dic_lista(listaUsuarios)) #Los envio al html

#ORDENA LOS USUARIOS
@router.route('/usuarios/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_usuarios(tipo, attr, metodo):
    uc = UsuarioControl()
    list = uc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": uc.to_dic_lista(list)}),
        200
    )
    
#BUSCA LOS USUARIOS
@router.route('/usuarios/busqueda/<tipo>/<data>/<attr>')
def buscar_usuarios(tipo, data, attr):
    uc = UsuarioControl()
    list = uc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": uc.to_dic_lista(list)}),
        200
    )

#################################################################################################################

#Presentar la lista de cuentas
@router.route('/administrador/gestionar_cuentas', methods=['GET'])
def gestionar_cuentas():
    cc = CuentaControl() #Creo un objeto de la clase UsuarioControl
    listaCuentas = cc._list() #Obtengo la lista de usuarios
    listaCuentas.sort_models("_id",1,4) #La ordeno por id para presentarla
    return render_template('administrador/crud/listaCuenta.html', lista = cc.to_dic_lista(listaCuentas)) #Los envio al html

#ORDENAR LAS CUENTAS
@router.route('/cuentas/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_cuentas(tipo, attr, metodo):
    cc = CuentaControl()
    list = cc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": cc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR CUENTAS
@router.route('/cuentas/busqueda/<tipo>/<data>/<attr>')
def buscar_cuentas(tipo, data, attr):
    cc = CuentaControl()
    list = cc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": cc.to_dic_lista(list)}),
        200
    )

# @router.route('/administrador/modificarCuenta', methods=['POST'])
# def modificarCuenta():
#     data = request.form
#     cc = CuentaControl()
#     cc.modificarDatoscuenta(data["id"], data["correo"], data["estado"])
#     return redirect(url_for('router.gestionar_cuentas'))

#####################################################################################################
#Presentar la lista de estudiantes
@router.route('/administrador/gestionar_estudiantes', methods=['GET'])
def gestionar_estudiantes():
    #Falta hacer que se presente el nombre y apellido del estudiante
    ec = EstudianteControl()
    listaEstudiantes = ec._list()
    listaEstudiantes.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaEstudiante.html', lista = ec.to_dic_lista(listaEstudiantes)) #Los envio al html
    

#ORDENAR LOS ESTUDIANTES
@router.route('/estudiantes/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_estudiantes(tipo, attr, metodo):
    ec = EstudianteControl()
    list = ec._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": ec.to_dic_lista(list)}),
        200
    )
    
#BUSCAR ESTUDIANTES
@router.route('/estudiantes/busqueda/<tipo>/<data>/<attr>')
def buscar_estudiantes(tipo, data, attr):
    ec = EstudianteControl()
    list = ec._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": ec.to_dic_lista(list)}),
        200
    )

########################################################################################################

#Presentar la lista de Administradores
@router.route('/administrador/gestionar_administradores', methods=['GET'])
def gestionar_administradores():
    #Falta hacer que se presente el nombre y apellido de los administradores
    ac = AdministradorControl()
    listaAdministradores = ac._list()
    listaAdministradores.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaAdministrador.html', lista = ac.to_dic_lista(listaAdministradores)) #Los envio al html
    

#ORDENAR LOS administradores
@router.route('/administradores/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_administradores(tipo, attr, metodo):
    ac = AdministradorControl()
    list = ac._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": ac.to_dic_lista(list)}),
        200
    )
    
#BUSCAR administradores
@router.route('/administradores/busqueda/<tipo>/<data>/<attr>')
def buscar_administradores(tipo, data, attr):
    ac = AdministradorControl()
    list = ac._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": ac.to_dic_lista(list)}),
        200
    )

########################################################################################################
#Presentar la lista de docentes
@router.route('/administrador/gestionar_docentes', methods=['GET'])
def gestionar_docentes():
    #Falta hacer que se presente el nombre y apellido del Docente
    dc = DocenteControl()
    listaDocentes = dc._list()
    listaDocentes.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaDocente.html', lista = dc.to_dic_lista(listaDocentes)) #Los envio al html
    

#ORDENAR LOS docentes
@router.route('/docentes/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_docentes(tipo, attr, metodo):
    dc = DocenteControl()
    list = dc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": dc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR docentes
@router.route('/docentes/busqueda/<tipo>/<data>/<attr>')
def buscar_docentes(tipo, data, attr):
    dc = DocenteControl()
    list = dc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": dc.to_dic_lista(list)}),
        200
    )


########################################################################################################

#Presentar la lista de permisos
@router.route('/administrador/gestionar_permisos', methods=['GET'])
def gestionar_permisos():
    pc = PermisoControl()
    listaPermisos = pc._list()
    listaPermisos.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaPermiso.html', lista = pc.to_dic_lista(listaPermisos)) #Los envio al html
    

#ORDENAR LOS ESTUDIANTES
@router.route('/permisos/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_permisos(tipo, attr, metodo):
    pc = PermisoControl()
    list = pc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": pc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR ESTUDIANTES
@router.route('/permisos/busqueda/<tipo>/<data>/<attr>')
def buscar_permisos(tipo, data, attr):
    pc = PermisoControl()
    list = pc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": pc.to_dic_lista(list)}),
        200
    )

########################################################################################################

#Presentar la lista de preguntas
@router.route('/administrador/gestionar_preguntas', methods=['GET'])
def gestionar_preguntas():
        #Falta que presente a que test esta asociada esta pregunta
    pc = PreguntaControl()
    listaPreguntas = pc._list()
    listaPreguntas.sort_models("_id",1,4)
    return render_template('administrador/crud/listaPregunta.html', lista = pc.to_dic_lista(listaPreguntas)) #Los envio al html
    

#ORDENAR preguntas
@router.route('/preguntas/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_preguntas(tipo, attr, metodo):
    pc = PreguntaControl()
    list = pc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": pc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR pregutnas
@router.route('/preguntas/busqueda/<tipo>/<data>/<attr>')
def buscar_preguntas(tipo, data, attr):
    pc = PreguntaControl()
    list = pc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": pc.to_dic_lista(list)}),
        200
    )

########################################################################################################

#Presentar la lista de roles
@router.route('/administrador/gestionar_roles', methods=['GET'])
#Falta poner que cuenta esta asociada a su rol correspondiente
def gestionar_roles():
    rc = RolControl()
    listaRoles = rc._list()
    listaRoles.sort_models("_id",1,4)
    return render_template('administrador/crud/listaRol.html', lista = rc.to_dic_lista(listaRoles)) #Los envio al html
    

#ORDENAR LOS roles
@router.route('/roles/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_roles(tipo, attr, metodo):
    rc = RolControl()
    list = rc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": rc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR roles
@router.route('/roles/busqueda/<tipo>/<data>/<attr>')
def buscar_roles(tipo, data, attr):
    rc = RolControl()
    list = rc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": rc.to_dic_lista(list)}),
        200
    )


########################################################################################################

#Presentar la lista de tests
@router.route('/administrador/gestionar_tests', methods=['GET'])
def gestionar_tests():
    tc = TestControl()
    listaTests = tc._list()
    listaTests.sort_models("_id",1,4)
    return render_template('administrador/crud/listaTest.html', lista = tc.to_dic_lista(listaTests)) #Los envio al html
    

#ORDENAR LOS roles
@router.route('/tests/ordenar/<tipo>/<attr>/<metodo>') 
def ordenar_tests(tipo, attr, metodo):
    tc = TestControl()
    list = tc._list()
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": tc.to_dic_lista(list)}),
        200
    )
    
#BUSCAR roles
@router.route('/tests/busqueda/<tipo>/<data>/<attr>')
def buscar_tests(tipo, data, attr):
    tc = TestControl()
    list = tc._list()
    if tipo == "1":
        list = list.lineal_binary_search_models(data, attr)
    elif tipo == "2":
        dato = list.binary_search_models(data, attr)
        list.clear
        if dato != -1:     
            list.addNode(dato)
        
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": tc.to_dic_lista(list)}),
        200
    )






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

