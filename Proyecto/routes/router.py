import os
from flask import Blueprint, app, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
import re
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
from controls.tda.notificacionControl import NotificacionControl
from controls.tda.cursoControl import CursoControl
from controls.tda.tareaControl import TareaControl
from controls.tda.entregaControl import EntregaControl
from flask import send_from_directory, abort, current_app
import os
import json
import urllib.parse
import ast
import re
from flask_login import login_required
from flask_login import login_user, logout_user, current_user
router = Blueprint('router', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads') 
ALLOWED_EXTENSIONS = {'pdf'}  


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
    login, rol, cursos, tiene, nombreRol, usuaario = cc.iniciarSesion(data["correo"], data["contrasenia"]) #Aqui llamo al metodo del controlador cc
    if login == -1:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('router.inicio'))
    elif login == 0:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('router.inicio'))
    else:
        print("###############################")
        print("Rol: ", rol)
        print(cursos.print)
        print("Tiene: ", tiene)
        print("NombreRol: ", nombreRol)
        print("Usuario: ", usuaario)
        login_user(usuaario)
        print("jejexd") 
        if rol == "Administrador":
            print("Estamos en administrador")
            return render_template('administrador/administrador.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuaario._nombre, apellidoU = usuaario._apellido, usuario = usuaario.serializable)
        elif rol == "Docente":
            return render_template('docente/docenteInicio.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuaario._nombre, apellidoU = usuaario._apellido, usuario = usuaario.serializable)
        elif rol == "Estudiante":
            return render_template('estudiante/inicioEstudiante.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuaario._nombre, apellidoU = usuaario._apellido, usuario = usuaario.serializable)
        else:
            flash('Esta cuenta no tiene un rol asignado', 'error')
            return render_template('inicio.html')




@router.route('/confirmar-regreso', methods=["GET", "POST"])
def confirmar_regreso():
    if current_user.is_authenticated:  
        return render_template('confirmar_regreso.html', nombre_usuario=current_user.name)
    else:
        return redirect(url_for('router.inicio')) 

@router.route('/proteccion')
@login_required  
def admin_dashboard():
    return render_template('admin/dashboard.html')

@router.route('/inicio/<roles>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=["GET"])
def regresarInicio(roles,usuario, nombreU, apellidoU, cursos, tiene):
    # cursos_string = cursos
    # cursos_decodificados = urllib.parse.unquote(cursos_string)
    # cursos_json = cursos_decodificados.replace("'", "\"")
    cursos_dic = eval(cursos)
    try:
        # cursos_dic = json.loads(cursos_json)
        if roles == "Administrador":
            return render_template('administrador/administrador.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos_dic, tiene = tiene, usuario = usuario)
        elif roles == "Docente":
            return render_template('docente/docenteInicio.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos_dic, tiene = tiene, usuario = usuario)
        elif roles == "Estudiante":
            return render_template('estudiante/inicioEstudiante.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos_dic, tiene = tiene, usuario = usuario)
        else:
            return render_template('inicio.html')
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON:", e)
    return render_template('inicio.html')
        
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
    usuarios = uc._list()
    usuarios.sort_models("_id", 1, 4)
    print(type(usuarios))
    legth = usuarios.getData(usuarios._length-1)._id
    cc.crearCuenta(data['correo'], data['contrasenia'], legth)
    cuentas = cc._list()
    cuentas.sort_models("_id", 1, 4)
    cuenta = cuentas.getData(cuentas._length-1)
    rc.crearRol(rol, cuenta._id)
    
    if rol == "Estudiante":
        ec = EstudianteControl()
        ec.agregarDatos(data["matricula"], data["contacto"], legth)
    elif rol == "Docente":
        dc = DocenteControl()
        dc.agregarTitulo(data["titulo"],  legth)
    elif rol == "Administrador":
        print("Estamos en administrador")
        ac = AdministradorControl()
        ac.agregarDatos(legth)
        
    flash('Cuenta creada con exito', 'success')
    return redirect(url_for('router.inicio'))
#---------------------------------------------Presentación-----------------------------------------------#
@router.route('/presentacion') 
def presentacion():
    return render_template('/presentacion/presentacion.html')



#------------ Vista Estudiante--------------------------------------------------#
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

# Estudiante Cursos y Tareas
@router.route('/estudiante/curso/inicio')
def tareas():
    return render_template('/estudiante/curso/cursoInicio.html')

@router.route('/estudiante/inicioTest/<roles>/<usuario>/<nombreU>/<apellidoU>/<tiene>/<cursos>', methods=['POST'])
def testInicio(roles, usuario, nombreU, apellidoU, tiene, cursos):
    cursos = eval(cursos)
    
    return render_template('/estudiante/testsE/inicioTest.html', roles = roles, usuario = usuario, nombreU = nombreU, apellidoU = apellidoU, tiene = tiene, cursos = cursos)


@router.route('/estudiante/inicioTestPost', methods=['POST'])
def testInicioPost():
    return render_template('/estudiante/testsE/inicioTest.html')


@router.route('/estudiante/subirTarea', methods=['POST'])
def subir_tarea():
    data = request.form
    cursos = eval(data["cursos"])
    usuario = data["usuario"]
    #Pasamos el string (usuario) a un diccionario 
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    tc = TareaControl()
    ee = EntregaControl()
    ac = AsignacionControl()
    tarea = "Sin tarea"
    entrega = "Sin entrega"
    entregas = ee._list()
    idAsignacion = "Sin asignacion"
    if not tc._list().isEmpty:
        tarea = tc._list().binary_search_models_id(data["idTarea"], "_id")
        if tarea == -1:
            tarea = "Sin tarea"
        asignaciones = ac._list()
        if not asignaciones.isEmpty:
            asignaciones = asignaciones.lineal_binary_search_models_id(data["idCurso"], "_idCurso")
            if not asignaciones.isEmpty:
                for asignacion in asignaciones.toArray:
                    if tarea._idAsignacion == asignacion._id:
                        idAsignacion = asignacion._id
                        if not entregas.isEmpty:
                            entrega = entregas.binary_search_models_id(asignacion._id, "_idAsignacion")
                            if entrega != -1:
                                break    
                                           
    archivo_nombre = os.path.basename(tarea._ruta_pdf)
    archivo_entrega = "Sin entrega"
    if entrega != -1 and entrega != "Sin entrega":
        archivo_entrega = os.path.basename(entrega._ruta_pdf)
        entrega = entrega.serializable  
    else:
        entrega = "Sin entrega"
    return render_template('/estudiante/curso/subirTarea.html',  roles = data["roles"], usuario = usuario, idCurso = data["idCurso"], idTarea = data["idTarea"], cursos = cursos, tiene = data["tiene"], tarea = tarea.serializable, nombreU = usuario["nombre"], apellidoU = usuario["apellido"], archivo = archivo_nombre, entrega = entrega, archivo_entrega = archivo_entrega, idAsignacion = idAsignacion)

#/subirTareaPdf/{{roles}}/{{usuario}}/{{curso.id}}/{{idTarea}}/{{idAsignacion}}/{{cursos}}{{tiene}}
@router.route('/subirTareaPdf/<roles>/<usuario>/<idCurso>/<idTarea>/<idAsignacion>/<cursos>/<tiene>', methods=['POST'])
def subirTareaPdf(roles, usuario,idCurso,idTarea, idAsignacion, cursos, tiene):
    cursos = eval(cursos)
    #Pasamos el string (usuario) a un diccionario 
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    ec = EstudianteControl()
    estudiantes = ec._list()
    fecha = datetime.now()
    fecha = fecha.strftime("%d/%m/%Y")
    permiso = 1
    comentario = "Sin comentario"
    estado = 1
    archivo = request.files['archivo']  
    if not archivo.filename == '':
        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(os.path.join(UPLOAD_FOLDER, archivo.filename))
    
    bandera = False
    entrega = "Sin entrega"
    if not estudiantes.isEmpty:
        estudiante = estudiantes.binary_search_models_id(usuario["id"], "_idUsuario")
        if estudiante != -1:
            if not archivo.filename == '':
                ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
                archivo.save(os.path.join(UPLOAD_FOLDER, archivo.filename))   
                ecd = EntregaControl()
                ecd.crearEntrega(ruta, estado, None, comentario, fecha, permiso, idAsignacion, estudiante._id)
                bandera = True
                entregas = ecd._list()
                entregas.sort_models("_id", 1, 4)
                entrega = entregas.getData(entregas._length-1)
    if bandera:
        flash('Entrega realizada con exito', 'success')
        tc = TareaControl()
        tarea = tc._list().binary_search_models_id(idTarea, "_id")
        if tarea != -1:
            archivo_nombre = os.path.basename(tarea._ruta_pdf)
            tarea = tarea.serializable
        archivo_entrega = os.path.basename(entrega._ruta_pdf)
        entrega = entrega.serializable
        return render_template('/estudiante/curso/subirTarea.html',  roles = roles, usuario = usuario, idCurso = idCurso, idTarea = idTarea, cursos = cursos, tiene = tiene, tarea = tarea, nombreU = usuario["nombre"], apellidoU = usuario["apellido"], archivo = archivo_nombre, entrega = entrega, archivo_entrega = archivo_entrega, idAsignacion = idAsignacion)



# Estudiante Tests
@router.route('/estudiante/resultado/ver')
def ver_resultado():
    return render_template('/estudiante/testsE/resultado.html')


@router.route('/estudiante/curso/ver/<roles>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['POST'])
def verCursoEstudiantePost(roles, usuario,nombreU, apellidoU, cursos, tiene):
    data = request.form
    id = data["idCurso"]
    cursos = eval(cursos)
    cc = CursoControl()
    ac= AsignacionControl()
    tc = TareaControl()
    curso = cc._list().binary_search_models(id, "_id")
    asignaciones = ac._list().lineal_binary_search_models(id, "_idCurso")
    tareas = Linked_List()
    for asignacion in asignaciones.toArray:
        tarea = tc._list().binary_search_models(str(asignacion._id), "_idAsignacion")
        tareas.addNode(tarea)
    
    return render_template('/estudiante/curso/curso.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, curso = curso.serializable, usuario = usuario, tareas = tc.to_dic_lista(tareas))
    






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
@login_required
def logout():
    logout_user()  
    return render_template("inicio.html")

@router.route('/estudiante/asignarEstudiante', methods=['POST'])
def asignarEstudiante():
    estudiantes_seleccionados = request.form.getlist('estudiantes')
    
    
    return render_template('/administrador/asignarCurso.html')



#------------------------------------------------Vista Docente----------------------------------------------------------------#
@router.route('/docente')
def docente():
    return render_template('/docente/docente.html')


@router.route('/docenteInicio', methods=['GET'])
def docenteInicio():
    return render_template('/docente/docenteCursos.html')



#INICIO 
@router.route('/docenteAd', methods=['GET'])
def docenteAd():
    return render_template('/docente/asignacion.html')


@router.route('/listaEstudiantes', methods=['GET'])
def verListaE():
    return render_template('/docente/crud/listaEstudiantes.html')   

@router.route('/tarea', methods=['GET'])
def asignarTarea():
    return render_template('/docente/asignarTarea.html')


#_____________________________________________DOCENTES VISTAS - DARWIN - DRAW_____________________________________________________#
@router.route('/docente/lista/tareas/test', methods=['GET'])
def listaTareas():
    return render_template('/docente/crud/listaTareasDocentes.html')

#/docente/lista/tareas/presentadas/{{roles}}/{{usuario}}/{{idCurso}}/{{tarea.id}}/{{cursos}}/{{tiene}}
@router.route('/docente/lista/tareas/presentadas', methods=['POST'])
def tareasPresentadas():
    data = request.form
    cursos = eval(data["cursos"])
    usuario = data["usuario"]
    #Pasamos el string (usuario) a un diccionario 
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    tc = TareaControl()
    ec = EstudianteControl()
    estudiantes = ec._list().lineal_binary_search_models(str(data["idCurso"]), "_idCurso")
    tarea = tc._list().binary_search_models(data["idTarea"], "_id")
    archivo_nombre = os.path.basename(tarea._ruta_pdf)

    
    return render_template('docente/crud/listaTareasPresentadas.html', roles = data["roles"], usuario = usuario, idCurso = data["idCurso"], idTarea = data["idTarea"], cursos = cursos, tiene = data["tiene"], tarea = tarea.serializable, estudiantes = ec.to_dic_lista(estudiantes), nombreU = usuario["nombre"], apellidoU = usuario["apellido"], archivo = archivo_nombre)

@router.route('/descargasEntrega/<idEntrega>')
def descargarArchivoEntrega(idEntrega):
    ec = EntregaControl()
    entrega = ec._list().binary_search_models_id(idEntrega, "_id")
    filename = os.path.basename(entrega._ruta_pdf)
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    try:
        return send_from_directory(upload_folder, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)



@router.route('/descargas/<idTarea>')
def descargarArchivo(idTarea):
    tc = TareaControl()
    tarea = tc._list().binary_search_models(idTarea, "_id")
    filename = os.path.basename(tarea._ruta_pdf)
    upload_folder = os.path.join(current_app.root_path, 'uploads') 
    try:
        return send_from_directory(upload_folder, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@router.route('/docente/lista/test/presentadas', methods=['GET']) 
def testPresentados():
    return render_template('docente/crud/listaTestPresentados.html')

#----------------------------------------------------------------------------------------------------------------------------------#
@router.route('/docente/crearAsignacion/<roles>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['GET'])
def crearTarea(roles, nombreU, apellidoU,cursos, tiene):
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
    

    return render_template('/docente/crearAsignacion.html', cursos = cursos_lista, estudiantes = ec.to_dic_lista(listaEst), usuarios = uc.to_dic_lista(lista), roles = roles, nombreU = nombreU, apellidoU = apellidoU, tiene = tiene)


@router.route('/docente/crearTareaGet/<roles>/<idCurso>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['GET'])
def crearTareaGet(roles, idCurso, usuario ,nombreU, apellidoU, cursos, tiene):
    cursos = eval(cursos)
    return render_template('/docente/crearTarea.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, idCurso = idCurso, usuario = usuario)

@router.route('/docente/crearTareaPost/<roles>/<idCurso>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['POST'])
def crearTareaPost(roles, idCurso, usuario, nombreU, apellidoU, cursos, tiene):
    data = request.form
    archivo = request.files['archivo']
    cursos = eval(cursos)
    
        
    if not archivo.filename == '':
        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(os.path.join(UPLOAD_FOLDER, archivo.filename))
        
    fecha_objetoUno = datetime.strptime(data["fechaInicio"], "%Y-%m-%d")
    fecha_objetoDos = datetime.strptime(data["fechaFin"], "%Y-%m-%d")
    fecha_formateadaUno = fecha_objetoUno.strftime("%d/%m/%Y")
    fecha_formateadaDos = fecha_objetoDos.strftime("%d/%m/%Y")
    fechaInicio = str(fecha_formateadaUno)
    fechaFin = str(fecha_formateadaDos)
        
    ac = AsignacionControl()
    dc = DocenteControl()
    nc = NotificacionControl()
    tc = TareaControl()
    ec = EstudianteControl()
    uc = UsuarioControl()
    cc = CuentaControl()

    #Pasamos el string (usuario) a un diccionario 
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    docente = dc._list().binary_search_models(usuario["id"], "_idUsuario")
    fechaActual = datetime.now()
    fechaActual = fechaActual.strftime("%d/%m/%Y")
    fechaActual = str(fechaActual)
    hora = datetime.now()
    hora = hora.strftime("%H:%M:%S")
    hora = str(hora)
    
    estudiantes = ec._list().lineal_binary_search_models(str(idCurso), "_idCurso")
    
    usuarios = uc._list()
    
    for est in estudiantes.toArray:
        persona = usuarios.binary_search_models(est._idUsuario, "_id")
        if persona != -1:
            cuenta = cc._list().binary_search_models(persona._id, "_idUsuario")
            if cuenta != -1:
                nc.crearNotificacion("Nueva Tarea", "Se ha asignado una tarea", fechaActual, hora, cuenta._id)
    
    notificaciones = nc._list()
    notificaciones.sort_models("_id", 1, 4)
    notificacion = notificaciones.getData(notificaciones._length-1)
        
    ac.crearAsignacion(fechaInicio, fechaFin, "Asignado", 1, None, idCurso, docente._id, notificacion._id)
    
    asignaciones = ac._list()
    asignaciones.sort_models("_id", 1, 4)
    asignacion = asignaciones.getData(asignaciones._length-1)
    
    tc.crearTarea(data["titulo"], data["descripcion"], 1,asignacion._id, ruta)
    
    return render_template('/docente/docenteInicio.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, usuario = usuario)

@router.route('/docente/crearTestGet/<roles>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['GET'])
def crearTestGet(roles, nombreU, apellidoU, cursos, tiene):
    cursos = eval(cursos)
    return render_template('/docente/crearTest.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene)

@router.route('/docente/curso/ver/<roles>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['POST'])
def verCursoDocentePost(roles, usuario,nombreU, apellidoU, cursos, tiene):
    data = request.form
    id = data["idCurso"]
    cursos = eval(cursos)
    cc = CursoControl()
    ac= AsignacionControl()
    tc = TareaControl()
    print("ID: ", id)
    curso = cc._list().binary_search_models_id(id, "_id")
    print("Curso: ", curso)
    curso = curso.serializable
    asignaciones = ac._list().lineal_binary_search_models_id(id, "_idCurso")
    tareas = Linked_List()
    for asignacion in asignaciones.toArray:
        tarea = "Sin tarea"
        if not tc._list().isEmpty:
            tarea = tc._list().binary_search_models_id(asignacion._id, "_idAsignacion")
            tareas.addNode(tarea)
    
    return render_template('/docente/crud/listaTareasDocentes.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, curso = curso, usuario = usuario, tareas = tc.to_dic_lista(tareas))
#---------------------------------------------Administrador-----------------------------------------------------#
@router.route('/administrador', methods=['GET'])
def administrador():
    return render_template('administrador/administrador.html')

#################################################################################################################
#Presentar la lista de usuarios
@router.route('/administrador/gestionar_usuarios/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
@login_required
def gestionar_usuarios(roles, nombreU, apellidoU):
    uc = UsuarioControl() #Creo un objeto de la clase UsuarioControl
    listaUsuarios = uc._list() #Obtengo la lista de usuarios
    listaUsuarios.sort_models("_id",1,4) #La ordeno por id para presentarla
    return render_template('administrador/crud/listaUsuario.html', roles =roles, nombreU =nombreU, apellidoU =apellidoU, lista = uc.to_dic_lista(listaUsuarios)) 

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

@router.route('/administrador/modificarUsuario/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarCuentaVer(pos, roles, nombreU, apellidoU):
    uc = UsuarioControl()
    editarUsuario = uc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarUsuario.html', data=editarUsuario, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

@router.route('/modificar_usuario/<roles>/<nombreU>/<apellidoU>', methods=['POST'])
def modificarUsuarioAdmin(roles, nombreU, apellidoU):
    data = request.form
    uc = UsuarioControl()
    fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
    fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
    fecha_formateada = str(fecha_formateada)
    uc.modificarUsuario(data["id"], data["nombre"], data["apellido"], data["ci"], fecha_formateada, data["telefono"], data["direccion"])
    return redirect(url_for('router.gestionar_usuarios', roles = roles, nombreU = nombreU, apellidoU = apellidoU))

#################################################################################################################

#Presentar la lista de cuentas
@router.route('/administrador/gestionar_cuentas/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_cuentas(roles, nombreU, apellidoU):
    cc = CuentaControl() #Creo un objeto de la clase UsuarioControl
    listaCuentas = cc._list() #Obtengo la lista de usuarios
    listaCuentas.sort_models("_id",1,4) #La ordeno por id para presentarla
    return render_template('administrador/crud/listaCuenta.html', lista = cc.to_dic_lista(listaCuentas), roles = roles, apellidoU = apellidoU, nombreU = nombreU) #Los envio al html

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
@router.route('/administrador/gestionar_estudiantes/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_estudiantes(roles,nombreU, apellidoU):
    #Falta hacer que se presente el nombre y apellido del estudiante
    ec = EstudianteControl()
    listaEstudiantes = ec._list()
    listaEstudiantes.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaEstudiante.html', lista = ec.to_dic_lista(listaEstudiantes), roles = roles, nombreU = nombreU, apellidoU = apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_administradores/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_administradores(roles, nombreU, apellidoU):
    #Falta hacer que se presente el nombre y apellido de los administradores
    ac = AdministradorControl()
    listaAdministradores = ac._list()
    listaAdministradores.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaAdministrador.html', lista = ac.to_dic_lista(listaAdministradores), nombreU = nombreU, roles = roles, apellidoU = apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_docentes/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_docentes(roles, nombreU, apellidoU):
    #Falta hacer que se presente el nombre y apellido del Docente
    dc = DocenteControl()
    listaDocentes = dc._list()
    listaDocentes.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaDocente.html', lista = dc.to_dic_lista(listaDocentes), roles = roles, nombreU = nombreU, apellidoU = apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_permisos/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_permisos(roles, nombreU, apellidoU):
    pc = PermisoControl()
    listaPermisos = pc._list()
    listaPermisos.sort_models("_id",1,4) 
    return render_template('administrador/crud/listaPermiso.html', lista = pc.to_dic_lista(listaPermisos), roles = roles, nombreU = nombreU, apellidoU = apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_preguntas/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_preguntas(roles, nombreU, apellidoU):
        #Falta que presente a que test esta asociada esta pregunta
    pc = PreguntaControl()
    listaPreguntas = pc._list()
    listaPreguntas.sort_models("_id",1,4)
    return render_template('administrador/crud/listaPregunta.html', lista = pc.to_dic_lista(listaPreguntas), roles = roles, nombreU=nombreU, apellidoU = apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_roles/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
#Falta poner que cuenta esta asociada a su rol correspondiente
def gestionar_roles(roles, nombreU, apellidoU):
    rc = RolControl()
    listaRoles = rc._list()
    listaRoles.sort_models("_id",1,4)
    return render_template('administrador/crud/listaRol.html', lista = rc.to_dic_lista(listaRoles), roles = roles, nombreU=nombreU, apellidoU=apellidoU) #Los envio al html
    

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
@router.route('/administrador/gestionar_tests/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def gestionar_tests(roles, nombreU, apellidoU):
    tc = TestControl()
    listaTests = tc._list()
    listaTests.sort_models("_id",1,4)
    return render_template('administrador/crud/listaTest.html', lista = tc.to_dic_lista(listaTests), roles = roles, nombreU=nombreU, apellidoU=apellidoU) #Los envio al html
    

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

@router.route('/administrador/asignarCurso/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def asignarCurso(roles, nombreU, apellidoU):
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
    
    return render_template('administrador/asignarCurso.html', cursos = cc.to_dic_lista(cursos), estudiantes = ec.to_dic_lista(lista), roles= roles, nombreU = nombreU, apellidoU = apellidoU)

#---------------------------------------------Estadisticas-----------------------------------------------------#    
@router.route('/estadisticas', methods=['GET'])
def estadisticas():
    # Datos de ejemplo para las estadísticas del estudiante
    return render_template('estadisticas/estadisticasEstudiantes.html')

#_____________________________________________Perfil_____________________________________________________#

@router.route('/perfil/ver/<tiene>/<roles>/<nombreU>/<apellidoU>/<usuario>/<cursos>', methods=['GET', 'POST'])
def perfil_editar(tiene, roles, nombreU, apellidoU, usuario, cursos):
    cursos = eval(cursos)
    uc = UsuarioControl()
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    usuario = uc.obtener_usuario(usuario["id"])
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ci = request.form['ci']
        fechaNacimiento = request.form['fechaNacimiento']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        if uc.actualizar_usuario(usuario._id, nombre, apellido, ci, fechaNacimiento, telefono, direccion):
            flash('Información actualizada correctamente', 'success')
        else:
            flash('Error al actualizar la información', 'danger')
        return redirect(url_for('perfil_editar', tiene=tiene, roles=roles, nombreU=nombreU, apellidoU=apellidoU, usuario=json.dumps(usuario.serializable), cursos=str(cursos)))
    
    return render_template('administrador/perfil.html', cursos=cursos, data=usuario, tiene=tiene, roles=roles, nombreU=nombreU, apellidoU=apellidoU, usuario=usuario.serializable)
