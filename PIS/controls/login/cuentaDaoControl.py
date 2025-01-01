from typing import Type
from controls.dao.daoAdapter import DaoAdapter
from models.cuenta import Cuenta


class CuentaDaoControl(DaoAdapter):
    def __init__(self):
        super().__init__(Cuenta)
        self.__cuenta = None


    @property
    def _cuenta(self):
        if self.__cuenta is None:
            self.__cuenta = Cuenta()
        return self.__cuenta

    @_cuenta.setter
    def _cuenta(self, value):
        self.__cuenta = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._cuenta)
    
    def merge(self, pos):
        self._merge(self._cuenta, pos)
