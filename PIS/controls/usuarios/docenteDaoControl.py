from typing import Type
from controls.dao.daoAdapter import DaoAdapter
from models.docente import Docente

class DocenteControl(DaoAdapter):
    def __init__(self):
        super().__init__(Docente) 
        self.__docente = None

    @property
    def _docente(self):
        if self.__docente == None:
            self.__docente = Docente()
        return self.__docente

    @_docente.setter
    def _docente(self, value):
        self.__docente = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        self._save(self._docente)

    def merge(self, pos):
        self._merge(self._docente, pos)
