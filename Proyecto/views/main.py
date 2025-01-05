import sys
sys.path.append('..')
from controls.tda.permisoControl import PermisoControl

pc = PermisoControl()


pc._permiso._nombre = "Registrar"
pc._permiso._detalle = "Permite registrar usuarios en el sistema"
pc._permiso._estado = 1
pc.save
