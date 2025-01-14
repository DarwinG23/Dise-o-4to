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
# uc._usuario._nombre = "Alexander"
# uc._usuario._apellido = "Sanchez"
# uc._usuario._ci = "1104753890"
# uc._usuario._fechaNacimiento = "02/05/2004" #IMPORTANTE EL FORMATO ES DD/MM/YYYY
# uc._usuario._direccion = "Buenos Aires y 9 de Octubre" 
# uc._usuario._telefono = "980679607"
# uc.save

#SEGUNDO CREAMOS LA CUENTA
# cc._cuenta._correo = "alexander.sanchez@unl.edu.ec"
# cc._cuenta._contrasena = "1234"
# cc._cuenta._estado = 1
# cc._cuenta._idUsuario = 3
# cc.save

#TERCERO CREAMOS EL ROL
# rc._rol._nombre = "Docente"
# rc._rol._detalle = "Rol para los docentes"
# rc._rol._estado = 1
# rc._rol._idCuenta = 3
# rc.save


#CUARTO CREAMOS EL PERMISO  
# pc._permiso._nombre = "Registrar"
# pc._permiso._detalle = "Permite registrar usuarios en el sistema"
# pc._permiso._estado = 1
# pc._permiso._idRol = 1
# pc.save
