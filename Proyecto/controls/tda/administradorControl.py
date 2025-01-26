from controls.dao.daoAdapter import DaoAdapter
from models.administrador import Administrador

class AdministradorControl(DaoAdapter):
    def __init__(self):
        super().__init__(Administrador)
        self.__admnistrador = None

    @property
    def _administrador(self):
        if self.__admnistrador is None:
            self.__admnistrador = Administrador()
        return self.__admnistrador

    @_administrador.setter
    def _administrador(self, value):
        self.__admnistrador = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._administrador)
    
    def merge(self, pos):
        self._merge(self._administrador, pos)
        
    def agregarDatos(self, idUsuario):
        self._administrador._idUsuario = idUsuario
        self.save
    