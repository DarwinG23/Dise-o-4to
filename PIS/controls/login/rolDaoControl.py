from controls.dao.daoAdapter import DaoAdapter
from models.rol import Rol


class RolDaoControl(DaoAdapter):
    
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
    