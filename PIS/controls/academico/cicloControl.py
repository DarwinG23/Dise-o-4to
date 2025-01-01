from controls.dao.daoAdapter import DaoAdapter
from models.ciclo import Ciclo


class CicloControl(DaoAdapter):
    def __init__(self):
        super().__init__(Ciclo)
        self.__ciclo = None

    @property
    def _ciclo(self):
        if self.__ciclo is None:
            self.__ciclo = Ciclo()
        return self.__ciclo

    @_ciclo.setter
    def _ciclo(self, value):
        self.__ciclo = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._ciclo)
    
    def merge(self, pos):
        self._merge(self._ciclo, pos)


    
