from controls.dao.daoAdapter import DaoAdapter
from models.usuario import Usuario

class UsuarioControl(DaoAdapter):
    def __init__(self):
        super().__init__(Usuario)
        self.__usuario = None

    @property
    def _usuario(self):
        if self.__usuario is None:
            self.__usuario = Usuario()
        return self.__usuario

    @_usuario.setter
    def _usuario(self, value):
        self.__usuario = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._usuario)
    
    def merge(self, pos):
        self._merge(self._usuario, pos)
    