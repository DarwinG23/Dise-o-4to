
from controls.dao.daoAdapter import DaoAdapter
from models.servidor import Servidor

class ServidorControl(DaoAdapter):
    def __init__(self):
        super().__init__(Servidor)
        self.__servidor = None

    @property
    def _servidor(self):
        if self.__servidor is None:
            self.__servidor = Servidor()
        return self.__servidor
    
    @_servidor.setter
    def _servidor(self, value):
        self.__servidor = value

    def _lista(self):
        return self._list()
    
    @property
    def save (self):
        self._save(self._servidor)

    def merge(self, pos):
        self._merge(self._servidor, pos)
    