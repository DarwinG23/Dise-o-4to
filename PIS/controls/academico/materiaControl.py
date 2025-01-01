from controls.dao.daoAdapter import DaoAdapter
from models.materia import Materia

class MateriaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Materia)
        self.__materia = None

    @property
    def _materia(self):
        if self.__materia is None:
            self.__materia = Materia()
        return self.__materia

    @_materia.setter
    def _materia(self, value):
        self.__materia = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._materia)
    
    def merge(self, pos):
        self._merge(self._materia, pos)

