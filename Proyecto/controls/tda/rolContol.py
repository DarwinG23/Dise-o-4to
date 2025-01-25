from controls.dao.daoAdapter import DaoAdapter
from models.rol import Rol

class RolControl(DaoAdapter):
    def __init__(self):
        super().__init__(Rol)
        self.__rol = None

    @property
    def _rol(self):
        if self.__rol is None:
            self.__rol = Rol()
        return self.__rol

    @_rol.setter
    def _rol(self, value):
        self.__rol = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._rol)
    
    def merge(self, pos):
        self._merge(self._rol, pos)

    
    def crearRol(self, nombre, idCuenta):
        self._rol._nombre = nombre
        detalle = "Sin detelle"
        if nombre == "Administrador":
            detalle = "Rol con permisos de administrador"
        elif nombre == "Docente":
            detalle = "Rol con permisos de docente"
        elif nombre == "Estudiante":
            detalle = "Rol con permisos de estudiante"
        self._rol._detalle = detalle
        self._rol._estado = 1
        self._rol._idCuenta = idCuenta
        self.save
         
    