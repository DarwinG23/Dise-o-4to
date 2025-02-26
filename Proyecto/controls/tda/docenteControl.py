from controls.dao.daoAdapter import DaoAdapter
from models.docente import Docente


class DocenteControl(DaoAdapter):
    def __init__(self):
        super().__init__(Docente)
        self.__docente = None

    @property
    def _docente(self):
        if self.__docente is None:
            self.__docente = Docente()
        return self.__docente

    @_docente.setter
    def _docente(self, value):
        self.__docente = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._docente)
    
    def merge(self, pos):
        self._merge(self._docente, pos)
        
    def agregarTitulo(self, titulo, idUsuario):
        self._docente._titulo = titulo
        self._docente._idUsuario = idUsuario
    
        self.save

        
    