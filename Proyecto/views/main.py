import sys
sys.path.append('..')
from controls.tda.permisoControl import PermisoControl
from controls.tda.rolContol import RolControl
from controls.tda.cuentaControl import CuentaControl
from controls.tda.usuarioControl import UsuarioControl

pc = PermisoControl()
rc = RolControl()
cc = CuentaControl()
uc = UsuarioControl()

#PIMERO CREAMOS EL USUARIO
# uc._usuario._nombre = "Darwin"
# uc._usuario._apellido = "Sarango"
# uc._usuario._ci = "1105630030"
# uc._usuario._fechaNacimiento = "20/06/2004" #IMPORTANTE EL FORMATO ES DD/MM/YYYY
# uc._usuario._direccion = "Obrapia Menfis Central" 
# uc._usuario._telefono = "0964209135"
# uc.save

#SEGUNDO CREAMOS LA CUENTA
# cc._cuenta._correo = "darwin.a.sarango@unl.edu.ec"
# cc._cuenta._contrasena = "1234"
# cc._cuenta._estado = 1
# cc._cuenta._idUsuario = 1
# cc.save

#TERCERO CREAMOS EL ROL
# rc._rol._nombre = "Estudiante"
# rc._rol._detalle = "Rol para los estudiantes"
# rc._rol._estado = 1
# rc._rol._idCuenta = 1
# rc.save


#CUARTO CREAMOS EL PERMISO  
# pc._permiso._nombre = "Registrar"
# pc._permiso._detalle = "Permite registrar usuarios en el sistema"
# pc._permiso._estado = 1
# pc._permiso._idRol = 1
# pc.save
