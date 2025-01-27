import sys
sys.path.append('..')
from controls.tda.permisoControl import PermisoControl
from controls.tda.rolContol import RolControl
from controls.tda.cuentaControl import CuentaControl
from controls.tda.usuarioControl import UsuarioControl
from controls.tda.estudianteControl import EstudianteControl
from controls.tda.cursoControl import CursoControl
from controls.tda.docenteControl import DocenteControl


pc = PermisoControl()
rc = RolControl()
cc = CuentaControl()
uc = UsuarioControl()
ec = EstudianteControl()
cuc = CursoControl()

#PIMERO CREAMOS EL USUARIO
# uc._usuario._nombre = "Alexander"
# uc._usuario._apellido = "Sánchez"
# uc._usuario._ci = "1104753890"
# uc._usuario._fechaNacimiento = "08/09/2003" #IMPORTANTE EL FORMATO ES DD/MM/YYYY
# uc._usuario._direccion = "Calle 10 de agosto y 9 de octubre" 
# uc._usuario._telefono = "0980679607"
# uc.save

#SEGUNDO CREAMOS LA CUENTA
# cc._cuenta._correo = "alexander.a.sanchez@unl.edu.ec"
# cc._cuenta._contrasena = "1234"
# cc._cuenta._estado = 1
# cc._cuenta._idUsuario = 1
# cc.save

# TERCERO CREAMOS EL ROL
# rc._rol._nombre = "Docente"
# rc._rol._detalle = "Rol para los docentes"
# rc._rol._estado = 1
# rc._rol._idCuenta = 1
# rc.save


#CUARTO CREAMOS EL PERMISO  
# pc._permiso._nombre = "Registrar"
# pc._permiso._detalle = "Permite registrar usuarios en el sistema"
# pc._permiso._estado = 1
# pc._permiso._idRol = 1
# pc.save


#CREACION DE UN ESTUDIANTE
# ec._estudiante._matricula = "697692"
# ec._estudiante._contactoEmergencia = "0979411882"
# ec._estudiante._idCurso = 1
# ec._estudiante._idUsuario = 4
# ec.save

# # #CREAR CURSO
# cc = CursoControl()

# cc._curso._nombre = "Sin cursos"
# cc._curso._paralelo = "sin"
# cc._curso._numParticipantes = 0
# cc._curso._idDocente = 1
# cc.save


# #CREAR DOCENTE
# dc = DocenteControl()
# dc._docente._titulo = "Ingeniero en sistemas"
# dc._docente._idUsuario = 1
# dc.save
