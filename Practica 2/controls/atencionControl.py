from controls.dao.daoAdapter import DaoAdapter
from models.atencion import Atencion
from typing import Type

class AtencionControl(DaoAdapter):
    def __init__(self):
        super().__init__(Atencion)
        self.__atencion = None

    @property
    def _atencion(self):
        if self.__atencion is None:
            self.__atencion = Atencion()
        return self.__atencion
    
    @_atencion.setter
    def _atencion(self, value):
        self.__atencion = value

    def _lista(self):
        return self._list()
    
    @property
    def save (self):
        self._save(self._atencion)

    def merge(self, pos):
        self._merge(self._atencion, pos)



    