from typing import Type
from controls.dao.daoAdapter import DaoAdapter
from  models.cursa import Cursa

class CursaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Cursa) 
        self.__cursa = None

    @property
    def _cursa(self):
        if self.__cursa is None:
            self.__cursa = Cursa()
        return self.__cursa
    

    @_cursa.setter
    def _cursa(self, value):
        self.__cursa = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        self._save(self._cursa)

    def merge(self, pos):
        self._merge(self._cursa, pos)
