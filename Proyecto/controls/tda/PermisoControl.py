from controls.dao.daoAdapter import DaoAdapter
from models.permiso import Permiso


class PermisoControl(DaoAdapter):
    def __init__(self):
        super().__init__(Permiso)
        self.__permiso = None

    @property
    def _permiso(self):
        if self.__permiso is None:
            self.__permiso = Permiso()
        return self.__permiso

    @_permiso.setter
    def _permiso(self, value):
        self.__permiso = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._permiso)
    
    def merge(self, pos):
        self._merge(self._permiso, pos)
    