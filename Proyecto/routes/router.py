import os
from flask import Blueprint, app, jsonify, abort , request, render_template, redirect, make_response, url_for, flash, Flask
from flask_cors import CORS
import time, math, datetime
import random
import re
from abc import ABC, abstractmethod
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
from controls.tda.opcionControl import OpcionControl
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

@router.route('/login', methods=["POST"])
def login():
    data = request.form
    correo = data["correo"]

    # Validar que el correo tenga el dominio correcto
    if not correo.endswith("@unl.edu.ec"):
        flash('Solo se permite el acceso a correos institucionales (@unl.edu.ec)', 'error')
        return redirect(url_for('router.inicio'))

    cc = CuentaControl()
    login, rol, cursos, tiene, nombreRol, usuario = cc.iniciarSesion(data["correo"], data["contrasenia"]) #Aqui llamo al metodo del controlador cc
    if login == -1:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('router.inicio'))
    elif login == 0:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('router.inicio'))
    else:
        flash(f'Bienvenido {usuario._nombre} {usuario._apellido}', 'success')
        flash('Inicio exitoso', 'success')  # ✅ Nuevo flash

        login_user(usuario) 
        if rol == "Administrador":
            return render_template('administrador/administrador.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuario._nombre, apellidoU = usuario._apellido, usuario = usuario.serializable)
        elif rol == "Docente":
            return render_template('docente/docenteInicio.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuario._nombre, apellidoU = usuario._apellido, usuario = usuario.serializable)
        elif rol == "Estudiante":
            return render_template('estudiante/inicioEstudiante.html', cursos = cc.to_dic_lista(cursos), tiene = tiene, roles = nombreRol, nombreU = usuario._nombre, apellidoU = usuario._apellido, usuario = usuario.serializable)
        else:
            flash('Esta cuenta no tiene un rol asignado', 'error')
            return render_template('inicio.html')

#____________________Recuperar Contraseña_______________________#
@router.route('/recuperarCuenta', methods=['GET'])
def recuperarCuentaVer():
    return render_template('presentacion/recuperarCuenta.html')

@router.route('/recuperarContrasena', methods=['GET', 'POST'])
def recuperarCuenta():
    contrasena = None

    if request.method == 'POST':
        correo = request.form.get("correo")

        if not correo:
            return render_template('recuperarCuenta.html', error="Por favor, ingresa un correo válido.")

        cc = CuentaControl()
        cuenta = cc._list().binary_search_models(correo, "_correo")

        if cuenta == -1:
            return render_template('recuperarCuenta.html', error="El correo ingresado no está registrado.")

        contrasena = cuenta._contrasena  # Obtener la contraseña

    return render_template('presentacion/recuperarCuenta.html', contrasena=contrasena)



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
#-------------------------------Registro---------------------------------------------------------------#
     
@router.route('/registrarEstudiante')
def registrarEstudiante():
    return render_template('registro.html',usuario = "Estudiante")   

@router.route('/registrarDocente')
def registrarDocente():
    return render_template('registro.html',usuario = "Docente")

@router.route('/registrarAdministrador')
def registrarAdministrador():
    return render_template('registro.html',usuario = "Administrador") 

@router.route('/registrar/<rol>', methods=["GET", "POST"])
def registrar(rol):
    # Verificar el rol para redirigir a la vista correcta
    if rol == "Administrador":
        return render_template('registro.html', usuario="Administrador")
    elif rol == "Estudiante":
        return render_template('registro.html', usuario="Estudiante")
    elif rol == "Docente":
        return render_template('registro.html', usuario="Docente")
    else:
        flash("Rol no válido", "error")
        return redirect(url_for('router.inicio'))   
       
@router.route('/registro/<rol>', methods=["POST"])
def registro(rol):
    data = request.form
    uc = UsuarioControl()
    cc = CuentaControl()
    rc = RolControl()

    # Validación del correo electrónico
    correo = data["correo"]
    if not correo.endswith("@unl.edu.ec"):
        flash('Solo se permite el acceso a correos institucionales (@unl.edu.ec)', 'error')
        return redirect(url_for('router.registrar', rol=rol))  # Redirigir al formulario según el rol

    # Validación de la cédula
    cedula = data["ci"]
    if not Cedula.validar_cedula(cedula):
        flash('Cédula inválida. Verifique que tenga 10 dígitos y cumpla con los requisitos.', 'error')
        return redirect(url_for('router.registrar', rol=rol))  # Redirigir al formulario si la cédula es inválida

    # Convertir la cadena a un objeto datetime
    fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
    fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
    fecha_formateada = str(fecha_formateada)

    # Crear el usuario
    uc.crearUsuario(data["nombre"], data["apellido"], cedula, fecha_formateada, data['telefono'], data['direccion'])
    usuarios = uc._list()
    usuarios.sort_models("_id", 1, 4)
    legth = usuarios.getData(usuarios._length-1)._id
    cc.crearCuenta(data['correo'], data['contrasenia'], legth)
    
    # Crear la cuenta
    cuentas = cc._list()
    cuentas.sort_models("_id", 1, 4)
    cuenta = cuentas.getData(cuentas._length-1)
    rc.crearRol(rol, cuenta._id)
    
    # Registrar según el rol
    if rol == "Estudiante":
        ec = EstudianteControl()
        ec.agregarDatos(data["matricula"], data["contacto"], legth)
    elif rol == "Docente":
        dc = DocenteControl()
        dc.agregarTitulo(data["titulo"], legth)
    elif rol == "Administrador":
        ac = AdministradorControl()
        ac.agregarDatos(legth)

    flash('Cuenta creada con éxito', 'success')
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

#/estudiante/responderTest
@router.route('/estudiante/responderTest', methods=['POST'])
def responderTest():
    data = request.form
    cursos = eval(data["cursos"])
    usuario= data["usuario"]
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    tc = TestControl()
    ee = EntregaControl()
    ac = AsignacionControl()
    

    tests = tc._list()
    test = -1
    if not tests.isEmpty:
        test = tests.binary_search_models_id(data["idTest"], "_id")
    
    
    
    preguntas = test._preguntas
    preguntas.sort_models("_id", 1, 4)
    
    opcionesT = Linked_List()
    for pregunta in preguntas.toArray:
        opcionesP = pregunta._opciones
        for opcion in opcionesP.toArray:
            opcionesT.addNode(opcion)
    
    
    opcionesT.sort_models("_id", 1, 4)
    
    return render_template('/estudiante/testsE/test.html',  roles = data["roles"], usuario = usuario, cursos = cursos, tiene = data["tiene"], test = test.serializable, preguntas = tc.to_dic_lista(preguntas), opciones = tc.to_dic_lista(opcionesT), nombreU = usuario["nombre"], apellidoU = usuario["apellido"])
    


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
    testC = TestControl()
    print("ID CURSO: ", id)
    curso = cc._list().binary_search_models_id(id, "_id")
    if curso != -1:
        curso = curso.serializable
    asignaciones = ac._list().lineal_binary_search_models_id(id, "_idCurso")
    tareas = Linked_List()
    tests = Linked_List()
    for asignacion in asignaciones.toArray:
        tarea = tc._list().binary_search_models_id(asignacion._id, "_idAsignacion")
        if tarea != -1:
            tareas.addNode(tarea)
        #carga los tests
        test = testC._list().binary_search_models_id(asignacion._id, "_idAsignacion")
        if test != -1 and test._idAsignacion != None:
            tests.addNode(test)
            
    #imprime los tests
    print("AHORA SI Tests: ")
    tests.print
    
    return render_template('/estudiante/curso/curso.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, curso = curso, usuario = usuario, tareas = tc.to_dic_lista(tareas), tests = tc.to_dic_lista(tests))
    






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

# {{roles}}/{{curso}}/{{tiene}}/{{usuario}}
@router.route('/docente/test/ver/<roles>/<curso>/<tiene>/<seleccionados>/<usuario>', methods=['Post'])
def verTestsDocente(roles, curso,tiene,seleccionados,usuario):
    data = request.form
    tc = TestControl()
    cc = CursoControl()
    dc = DocenteControl()
    uc = UsuarioControl()
    cursos = cc._list()
    cursosDocente = Linked_List()
    ususarios = uc._list()
    docentes = dc._list()
    
    docente = -1
    usuario = -1
    idCurso = -1
    try:
        idCurso = curso._id
    except:
        idCurso = curso


    if not cursos.isEmpty and not docentes.isEmpty and not ususarios.isEmpty and idCurso != -1:
        
        cursoBd = cursos.binary_search_models_id(idCurso, "_id")
        if cursoBd != -1:
            docente = docentes.binary_search_models_id(cursoBd._idDocente, "_id")
            if docente != -1:
                usuario = ususarios.binary_search_models_id(docente._idUsuario, "_id")
                
   
    if usuario != -1:
        nombreU = usuario._nombre
        apellidoU = usuario._apellido
        usuario = usuario.serializable
        if not cursos.isEmpty and docente != -1:
            cursosDocente = cursos.lineal_binary_search_models_id(docente._id, "_idDocente")


    
    tests = tc._list()
    test = -1
    if not tests.isEmpty:
        test = tests.binary_search_models_id(data["idTest"], "_id")
    
    
    
    preguntas = test._preguntas
    preguntas.sort_models("_id", 1, 4)
    
    opcionesT = Linked_List()
    for pregunta in preguntas.toArray:
        opcionesP = pregunta._opciones
        for opcion in opcionesP.toArray:
            opcionesT.addNode(opcion)
    
    
    opcionesT.sort_models("_id", 1, 4)
    
    
    return render_template('/docente/test/test.html', cursos = cc.to_dic_lista(cursosDocente), roles = roles, curso = curso, tiene = tiene, usuario = usuario, nombreU = nombreU, apellidoU = apellidoU, test = test.serializable, preguntas = uc.to_dic_lista(preguntas), opciones = uc.to_dic_lista(opcionesT), seleccionados = seleccionados)



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

#/asignarTest/' + testId + '/{{roles}}/{{usuario}}/{{cursos}}/{{tiene}}/{{seleccionados}}
import json
import datetime
import html
@router.route('/asignarTest', methods=['POST'])
def asignarTest():
    data = request.form
    cursos = data["cursos"]
    #Pasamos el string (usuario) a un diccionario 
    usuario = data["usuario"]
    testId = data["testId"]
    seleccionados = data["seleccionados"]
    tiene = data["tiene"]
    roles = data["roles"]
    idCurso = data["idCurso"]
    
    usuario = html.unescape(usuario)  
    usuario = usuario.replace("'", '"')
    usuario = usuario.replace('datetime.datetime(', '"').replace(', 0, 0)', '"')
    usuario = json.loads(usuario)
    
    #Pasamos el string (cursos) a un diccionario
    cursos = html.unescape(cursos)
    cursos = cursos.replace("'", '"')
    cursos = json.loads(cursos)
    
    
    ids = []
    for i in seleccionados:
        if i.isdigit():
            ids.append(i)
            
    fecha = datetime.datetime.now()
    fecha = fecha.strftime("%d/%m/%Y")
    
    fechaDos = datetime.datetime.now()
    fechaDos = fechaDos.strftime("%d/%m/%Y")        
    
    #Creamos la asignacion
    ac = AsignacionControl()
    tc = TestControl()
    ec = EstudianteControl()
    dc = DocenteControl()
    pc = PreguntaControl()
    oc = OpcionControl()
    docente = dc._list().binary_search_models_id(usuario["id"], "_idUsuario")
    test = tc._list().binary_search_models_id(int(testId), "_id")
    if test != -1 and docente != -1:
        #recorre las ids
        for id in ids:
            estudiante = ec._list().binary_search_models_id(int(id), "_idUsuario")
            if estudiante != -1:
                ac.crearAsignacion(fecha, fechaDos, 1,1,estudiante._id,int(idCurso),docente._id,1)
                
    #obtengo el test 
    test = tc._list().binary_search_models_id(int(testId), "_id")
    if test != -1:
        #ordeno las asignaciones
        asignaciones = ac._list().lineal_binary_search_models_id(int(idCurso), "_idCurso")
        asignaciones.sort_models("_id", 1, 4)
        asignacion = asignaciones.getData(asignaciones._length-1)
        #creo un nuevo test
        tc.crearTest(test._nombre, test._descripcion, test._resultado, asignacion._id, None)
        #obtengo el test id del test creado
        tests = tc._list()
        tests.sort_models("_id", 1, 4)
        testNuevo = tests.getData(tests._length-1)
        
        preguntas = test._preguntas
        
        for pregunta in preguntas.toArray:
            #creo una nueva pregunta
            pc.crearPregunta(pregunta._pregunta, pregunta._estado,pregunta._respuesta, testNuevo._id)
            
            #obtengo la pregunta creada
            preguntas = pc._list()
            preguntas.sort_models("_id", 1, 4)
            preguntaNueva = preguntas.getData(preguntas._length-1)
            
            #obtengo las opciones de la pregunta
            opciones = pregunta._opciones
            for opcion in opciones.toArray:
                #creo una nueva opcion
                oc.crearOpcion(opcion._opcion, opcion._estado,opcion._valor, preguntaNueva._id)
        
        
        
        
    

    if isinstance(usuario, str):
        usuario = json.loads(usuario) 
        
    flash('Test asignado con exito', 'success') 
    return render_template('/docente/docenteInicio.html', roles = roles, usuario = usuario, cursos = cursos, tiene = tiene, seleccionados = seleccionados, testId = testId, nombreU = usuario["nombre"], apellidoU = usuario["apellido"])


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

#_____________________________________________DOCENTES VISTAS - DARWIN - DOCENTE / REGISTRO________________________________________#

@router.route('/administrador/crearDocente/ver/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def listaRegistroD(roles, nombreU, apellidoU):
    return render_template('administrador/crud/listaCrearRegistroDocente.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU)

@router.route('/crearDocente/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def crearDocente(roles, nombreU, apellidoU):
    data = request.form
    dc = DocenteControl()
    uc = UsuarioControl()
    rc = RolControl()
    # Convertir la cadena a un objeto datetime
    fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
    fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
    fecha_formateada = str(fecha_formateada)

    uc.crearUsuario(data["nombre"],data["apellido"], data['ci'], fecha_formateada, data['telefono'], data['direccion'])
    
    return redirect(url_for('router.gestionar_docentes', roles = roles, nombreU = nombreU, apellidoU = apellidoU))

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

@router.route('/docente/seleccionar/estudiante/<roles>/<usuario>/<cursos>/<tiene>/<idCurso>', methods=['GET'])
def seleccionarEstudiante(roles, usuario, cursos, tiene, idCurso):
    cursos = eval(cursos)
    ec = EstudianteControl()
    uc = UsuarioControl()
    estudiantes = ec._list().lineal_binary_search_models_id(idCurso, "_idCurso")
    if estudiantes == -1:
        estudiantes = Linked_List()
    
    usuarios = Linked_List()
    for estudiante in estudiantes.toArray:
        usuario = uc._list().binary_search_models_id(estudiante._idUsuario, "_id")
        if usuario != -1:
            usuarios.addNode(usuario)
    
    return render_template('/docente/seleccionarEstudiante.html', roles = roles, usuario = usuario, cursos = cursos, tiene = tiene, estudiantes = ec.to_dic_lista(estudiantes), idCurso = idCurso, usuarios = uc.to_dic_lista(usuarios))

@router.route('/docente/crearTestGet/<roles>/<usuario>/<cursos>/<tiene>', methods=['GET'])
def crearTestGet(roles, usuario, cursos, tiene):
    cursos = eval(cursos)
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    return render_template('/docente/crearTest.html', roles = roles, nombreU = usuario["nombre"], apellidoU = usuario["apellido"], cursos = cursos, tiene = tiene, usuario=usuario)

@router.route('/crearTestPost/<roles>/<usuario>/<cursos>/<tiene>', methods=['POST'])
def creartestPost(roles,usuario,cursos,tiene):
    data = request.form
    print("Datos recibidos en request.form:")
    for key in request.form:
        print(f"{key}: {request.form[key]}")
    pc = PreguntaControl()
    tc = TestControl()
    oc = OpcionControl()
    ac = AsignacionControl()
    dc = DocenteControl()
    nc = NotificacionControl()

    cursos = eval(cursos)
    
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    
    
    fecha_inicio = data["fechaInicio"]
    fecha_fin = data["fechaFin"]
    
    #formatea las fechas a dd/mm/yyyy
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    fecha_fin = fecha_fin.strftime("%d/%m/%Y")
    
    docente = dc._list().binary_search_models_id(usuario["id"], "_idUsuario")
    
    ac.crearAsignacion(fecha_inicio,fecha_fin,1,1,None,None,docente._id,None)
   
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")


    tc.crearTest(titulo, descripcion,None,None,None)

    preguntas = []
    contador = 1  
    
    tests = tc._list()
    test = -1
    if not tests.isEmpty:
        tests.sort_models("_id",1,4)
        test = tests.getData(tests._length-1)
    
    if test != -1:
        while True:
            pregunta_key = f"pregunta-{contador}"
            pregunta_texto = request.form.get(pregunta_key)

            if not pregunta_texto:
                break 
            
            pc.crearPregunta(pregunta_texto, 1,"Sin respuesta", test._id)
            preguntasBd = pc._list()
            if not preguntasBd.isEmpty:
                
                preguntasBd.sort_models("_id",1,4)
                pregunta = preguntasBd.getData(preguntasBd._length-1)
                if pregunta != -1:
                    respuestas = []
                    respuesta_contador = 1  

                    while True:
                        respuesta_key = f"respuesta-{contador}-{respuesta_contador}"
                        valor_key = f"valor-{contador}-{respuesta_contador}"

                        # Buscar respuestas en el request.form
                        if respuesta_key in request.form:
                            respuesta_texto = request.form[respuesta_key].strip()
                            respuesta_valor = request.form.get(valor_key, "0").strip()  # Valor por defecto 0

                            print(f"Guardando opción: {respuesta_texto} con valor {respuesta_valor}")
                            oc.crearOpcion(respuesta_texto, 1, int(respuesta_valor), pregunta._id)

                            respuestas.append({"texto": respuesta_texto, "valor": respuesta_valor})
                        else:
                            print(f"No se encontró {respuesta_key}, omitiendo.")

                        # Seguir buscando hasta que no haya más respuestas
                        respuesta_contador += 1
                        if respuesta_contador > 10:  # Un límite de seguridad para evitar bucles infinitos
                            break

                    preguntas.append({"pregunta": pregunta_texto, "respuestas": respuestas})
                    contador += 1
            
    return render_template('administrador/administrador.html', cursos = cursos, tiene = tiene, roles = roles, nombreU = usuario["nombre"], apellidoU = usuario["apellido"], usuario = usuario)

@router.route('/crearTestAdminGet/<roles>/<usuario>/<cursos>/<tiene>', methods=['GET'])
def crearTestGetAdmin(roles, usuario, cursos, tiene):
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    return render_template('/administrador/crearTest.html', roles = roles, usuario = usuario, cursos = cursos, tiene = tiene, nombreU = usuario['nombre'], apellidoU=usuario['apellido'])


@router.route('/crearTestAdminPost/<roles>/<usuario>/<cursos>/<tiene>', methods=['POST'])
def crearTestPostAdmin(roles,usuario,cursos,tiene):
    print("Datos recibidos en request.form:")
    for key in request.form:
        print(f"{key}: {request.form[key]}")
    pc = PreguntaControl()
    tc = TestControl()
    oc = OpcionControl()
    ac = AdministradorControl()
    cursos = eval(cursos)
    
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    fecha_inicio = None
    fecha_fin = None
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    admins = ac._list()

    if not admins.isEmpty:
        admin = ac._list().binary_search_models_id(usuario["id"], "_idUsuario")
    if admin != -1:
      tc.crearTest(titulo, descripcion,None,None,admin._id)

    preguntas = []
    contador = 1  
    
    tests = tc._list()
    test = -1
    if not tests.isEmpty:
        tests.sort_models("_id",1,4)
        test = tests.getData(tests._length-1)
    
    if test != -1:
        while True:
            pregunta_key = f"pregunta-{contador}"
            pregunta_texto = request.form.get(pregunta_key)

            if not pregunta_texto:
                break 
            
            pc.crearPregunta(pregunta_texto, 1,"Sin respuesta", test._id)
            preguntasBd = pc._list()
            if not preguntasBd.isEmpty:
                
                preguntasBd.sort_models("_id",1,4)
                pregunta = preguntasBd.getData(preguntasBd._length-1)
                if pregunta != -1:
                    respuestas = []
                    respuesta_contador = 1  

                    while True:
                        respuesta_key = f"respuesta-{contador}-{respuesta_contador}"
                        valor_key = f"valor-{contador}-{respuesta_contador}"

                        # Buscar respuestas en el request.form
                        if respuesta_key in request.form:
                            respuesta_texto = request.form[respuesta_key].strip()
                            respuesta_valor = request.form.get(valor_key, "0").strip()  # Valor por defecto 0

                            print(f"Guardando opción: {respuesta_texto} con valor {respuesta_valor}")
                            oc.crearOpcion(respuesta_texto, 1, int(respuesta_valor), pregunta._id)

                            respuestas.append({"texto": respuesta_texto, "valor": respuesta_valor})
                        else:
                            print(f"No se encontró {respuesta_key}, omitiendo.")

                        # Seguir buscando hasta que no haya más respuestas
                        respuesta_contador += 1
                        if respuesta_contador > 10:  # Un límite de seguridad para evitar bucles infinitos
                            break

                    preguntas.append({"pregunta": pregunta_texto, "respuestas": respuestas})
                    contador += 1
            
    return render_template('administrador/administrador.html', cursos = cursos, tiene = tiene, roles = roles, nombreU = usuario["nombre"], apellidoU = usuario["apellido"], usuario = usuario)



@router.route('/docente/curso/ver/<roles>/<usuario>/<nombreU>/<apellidoU>/<cursos>/<tiene>', methods=['POST'])
def verCursoDocentePost(roles, usuario,nombreU, apellidoU, cursos, tiene):
    data = request.form
    id = data["idCurso"]
    cursos = eval(cursos)
    cc = CursoControl()
    ac= AsignacionControl()
    tc = TareaControl()
    testc = TestControl()
    curso = cc._list().binary_search_models_id(id, "_id")
    if curso != -1:
        curso = curso.serializable
    asignaciones = ac._list().lineal_binary_search_models_id(id, "_idCurso")
    tareasBd = tc._list()
    testsBd = testc._list()
    tareas = Linked_List()
    examenes = Linked_List()
    #imprimiendo las asignaciones
    print("######")
    asignaciones.print
    for asignacion in asignaciones.toArray:
        tarea = "Sin tarea"
        examen = "Sin test"
        if not tareasBd.isEmpty:
            tarea = tareasBd.binary_search_models_id(asignacion._id, "_idAsignacion")
            if tarea != -1:
                tareas.addNode(tarea)
        if not testsBd.isEmpty:
            examen = testsBd.binary_search_models_id(asignacion._id, "_idAsignacion")
            if examen != -1 and examen._idAdministrador != None:
               examenes.addNode(examen)
               
    print("######TESTS")
    print("######TESTS")
    print("######TESTS")
    print("######TESTS")
    examenes.print
    print("######TESTS")
    print("######TESTS")
    print("######TESTS")
    print("######TESTS")
    print("######TESTS")
    
    #imprime la longitud de examenes
    print("Longitud de examenes: ", examenes._length)
    print("############")
    
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    
    return render_template('/docente/crud/listaTareasDocentes.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU, cursos = cursos, tiene = tiene, curso = curso, usuario = usuario, tareas = tc.to_dic_lista(tareas), tests = testc.to_dic_lista(examenes))

@router.route('/agregarTest/<roles>/<idCurso>/<usuario>/<tiene>', methods=['POST'])
def agregarTest(roles, idCurso,usuario, tiene):
    cc = CursoControl()
    dc = DocenteControl()
    uc = UsuarioControl()
    cursos = cc._list()
    docente = -1
    if not cursos.isEmpty:
        curso = cursos.binary_search_models_id(idCurso, "_id")
        docente = dc._list().binary_search_models_id(curso._idDocente, "_id")
        
    if docente != -1:
        usuario = uc._list().binary_search_models_id(docente._idUsuario, "_id")
        usuario = usuario.serializable
        
        
    data = request.form
    cursos = eval(data["cursos"])

    
    tc = TestControl()
    tests = tc._list()
    testsAdmin = Linked_List()
    if not tests.isEmpty:
        for test in tests.toArray:
            if test._idAdministrador != None:
                testsAdmin.addNode(test)
    
    bandera ="Verdadero"
    if testsAdmin.isEmpty:
        bandera = "Falso"

        
    return render_template('docente/agregarTest.html', tests = tc.to_dic_lista(testsAdmin), bandera = bandera, usuario = usuario, nombreU=usuario["nombre"], apellidoU = usuario["apellido"], roles = roles, cursos = cursos, tiene = tiene, idCurso = idCurso, seleccionados = data["usuarios_seleccionados"])




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
    
#ORDENA LOS USUARIOS
@router.route('/usuarios/ordenar/<tipo>/<attr>/<metodo>/<usuarios>') 
def ordenar_usuarios_docente(tipo, attr, metodo,usuarios):
    usuarios = eval(usuarios)
    uc = UsuarioControl()
    list = Linked_List()
    for usuario in usuarios:
        list.addNode(usuario)
    list.sort_models(attr,int(tipo),int(metodo))
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": uc.to_dic_lista(list)}),
        200
    )


    
#BUSCA LOS USUARIOS
@router.route('/usuarios/busqueda/<tipo>/<data>/<attr>/<usuarios>')
def buscar_usuarios_docente(tipo, data, attr, usuarios):
    uc = UsuarioControl()
    usuarios = eval(usuarios)
    list = Linked_List()
    for usuario in usuarios:
        if usuario[attr] == data:
            list.addNode(usuario)
            
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


# @router.route('/modificar_usuario/<roles>/<nombreU>/<apellidoU>', methods=['POST'])
# def modificarUsuarioAdmin(roles, nombreU, apellidoU):
#     data = request.form
#     uc = UsuarioControl()
#     fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
#     fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
#     fecha_formateada = str(fecha_formateada)
#     uc.modificarUsuario(data["id"], data["nombre"], data["apellido"], data["ci"], fecha_formateada, data["telefono"], data["direccion"])
#     return redirect(url_for('router.gestionar_usuarios', roles = roles, nombreU = nombreU, apellidoU = apellidoU))

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
    uc = UsuarioControl()
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

@router.route('/estadisticas/individual', methods=['GET'])
def estadisticas_individual():
    return render_template('estadisticas/estadisticasIndividual.html')

@router.route('/perfil/ver/<tiene>/<roles>/<nombreU>/<apellidoU>/<usuario>/<cursos>', methods=['GET', 'POST'])
def perfil_editar(tiene, roles, nombreU, apellidoU, usuario, cursos):
    cursos = eval(cursos)
    uc = UsuarioControl()
    usuario = re.sub(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)", r'"\1-\2-\3 \4:\5"', usuario)
    usuario = usuario.replace("'", '"')
    usuario = json.loads(usuario)
    usuario = uc.obtener_usuario(usuario["id"])
    return render_template('administrador/perfil.html', cursos=cursos, data=usuario, tiene=tiene, roles=roles, nombreU=nombreU, apellidoU=apellidoU, usuario=usuario.serializable)


#___________________Crear Usuario_______________________# Funciona Bien

@router.route('/administrador/crearUsuario/ver/<roles>/<nombreU>/<apellidoU>', methods=['GET'])
def crearUsuarioVer(roles, nombreU, apellidoU):
    return render_template('administrador/crud/crear/crearUsuario.html', roles = roles, nombreU = nombreU, apellidoU = apellidoU)


@router.route('/crear_usuario/<roles>/<nombreU>/<apellidoU>', methods=['POST'])
def crearUsuarioAdmin(roles, nombreU, apellidoU):
    data = request.form
    uc = UsuarioControl()

    fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
    fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
    fecha_formateada = str(fecha_formateada)
    uc.crearUsuario(data["nombre"], data["apellido"], data["ci"], fecha_formateada, data["telefono"], data["direccion"])
    return redirect(url_for('router.gestionar_usuarios', roles = roles, nombreU = nombreU, apellidoU = apellidoU))

#___________________Modificar Usuario_______________________#

@router.route('/administrador/modificarUsuario/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarUsuarioVer(pos, roles, nombreU, apellidoU):
    uc = UsuarioControl()
    editarUsuario = uc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarUsuario.html', data=editarUsuario, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

# @router.route('/modificar_usuario/<roles>/<nombreU>/<apellidoU>', methods=['POST'])
# def modificarUsuarioAdmin(roles, nombreU, apellidoU):
#     data = request.form
#     uc = UsuarioControl()
#     fecha_objeto = datetime.strptime(data["fechaNacimiento"], "%Y-%m-%d")
#     fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
#     fecha_formateada = str(fecha_formateada)
#     uc.modificarUsuario(data["id"], data["nombre"], data["apellido"], data["ci"], fecha_formateada, data["telefono"], data["direccion"])
#     return redirect(url_for('router.gestionar_usuarios', roles = roles, nombreU = nombreU, apellidoU = apellidoU))

#___________________Modificar Cuenta_______________________#
@router.route('/administrador/modificarCuenta/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarCuentaVer(pos, roles, nombreU, apellidoU):
    cc = CuentaControl()
    editarCuenta = cc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarCuenta.html', data=editarCuenta, roles = roles, nombreU = nombreU, apellidoU = apellidoU)


#___________________Modificar Estudiante_______________________#
@router.route('/administrador/modificarEstudiante/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarEstudianteVer(pos, roles, nombreU, apellidoU):
    ec = EstudianteControl()
    editarEstudiante = ec._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarEstudiante.html', data=editarEstudiante, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

#___________________Modificar Administrador_______________________#
@router.route('/administrador/modificarAdministrador/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarAdministradorVer(pos, roles, nombreU, apellidoU):
    ac = AdministradorControl()
    editarAdministrador = ac._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarAdministrador.html', data=editarAdministrador, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

#___________________Modificar Docente_______________________#
@router.route('/administrador/modificarDocente/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarDocenteVer(pos, roles, nombreU, apellidoU):
    dc = DocenteControl()
    editarDocente = dc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarDocente.html', data=editarDocente, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

#___________________Modificar Permiso_______________________#
@router.route('/administrador/modificarPermiso/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarPermisoVer(pos, roles, nombreU, apellidoU):
    pc = PermisoControl()
    editarPermiso = pc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarPermiso.html', data=editarPermiso, roles = roles, nombreU = nombreU, apellidoU = apellidoU)

#___________________Modificar Rol_______________________#
@router.route('/administrador/modificarRol/ver/<roles>/<nombreU>/<apellidoU>/<pos>', methods=['GET'])
def modificarRolVer(pos, roles, nombreU, apellidoU):
    rc = RolControl()
    editarRol = rc._list().binary_search_models(int(pos), "_id")
    return render_template('administrador/crud/editar/editarRol.html', data=editarRol, roles = roles, nombreU = nombreU, apellidoU = apellidoU)



#--------------------------------------------Administrador/Vista/Darwin- Draw-----------------------------------------------------#

@router.route('/prueba01', methods=['GET'])
def prueba01():
    return render_template('administrador/crud/pruebas01.html')

@router.route('/prueba02', methods=['GET'])
def prueba02():
    return render_template('administrador/crud/pruebas02.html')


@router.route('/prueba')   
def prueba(): 
   return render_template('perfil.html')

#--------------------------------------------Administrador/Vista/Darwin- Draw-----------------------------------------------------#
