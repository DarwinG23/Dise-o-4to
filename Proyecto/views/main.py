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


uc._usuario._nombre = "Darwin"
uc._usuario._apellido = "Granda"
uc._usuario.__ci = "1106006123"
uc._usuario._fechaNacimiento = "1999-06-12"
uc._usuario._direccion = "Ciudad Alegria"
uc._usuario._telefono = "0979411882"
uc.save


# pc._permiso._nombre = "Registrar"
# pc._permiso._detalle = "Permite registrar usuarios en el sistema"
# pc._permiso._estado = 1
# pc.save
