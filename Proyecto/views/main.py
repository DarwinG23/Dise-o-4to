import sys
sys.path.append('..')
from controls.tda.administradorControl import AdministradorControl
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
# uc._usuario._apellido = "Sanchez"
# uc._usuario._ci = "1104753890"
# uc._usuario._fechaNacimiento = "06/06/2003" #IMPORTANTE EL FORMATO ES DD/MM/YYYY
# uc._usuario._direccion = "Tierras coloradas" 
# uc._usuario._telefono = "0980679607"
# uc.save

#SEGUNDO CREAMOS LA CUENTA
# cc._cuenta._correo = "admin.darwin@unl.edu.ec"
# cc._cuenta._contrasena = "1234"
# cc._cuenta._estado = 1
# cc._cuenta._idUsuario = 4
# cc.save

# TERCERO CREAMOS EL ROL
# rc._rol._nombre = "Administrador"
# rc._rol._detalle = "Rol para los administradores del sistema"
# rc._rol._estado = 1
# rc._rol._idCuenta = 3
# rc.save


#CUARTO CREAMOS EL PERMISO  
# pc._permiso._nombre = "Registrar"
# pc._permiso._detalle = "Permite registrar usuarios en el sistema"
# pc._permiso._estado = 1
# pc._permiso._idRol = 1
# pc.save


#CREACION DE ADMINISTRADOR
# ac = AdministradorControl()
# ac._administrador._idUsuario = 4
# ac.save

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
